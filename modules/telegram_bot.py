import os
import re
import threading
import subprocess
import telebot
from telebot import types
from flask import Blueprint, jsonify
from modules.system_info import get_battery, get_storage, get_ram

bp = Blueprint("telegram_bot", __name__, url_prefix="/api/telegram")

# --- CONFIGURATION ---
def required_env(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Required environment variable {name} is not set")
    return value


BOT_TOKEN = required_env("BOT_TOKEN")
try:
    ALLOWED_USER_ID = int(required_env("ALLOWED_USER_ID"))
except ValueError as exc:
    raise RuntimeError("ALLOWED_USER_ID must be a numeric Telegram user ID") from exc
DOWNLOAD_DIR = required_env("DOWNLOAD_DIR")
TRANSMISSION_REMOTE = required_env("TRANSMISSION_REMOTE")

MAGNET_REGEX = re.compile(r"(magnet:\?xt=urn:[a-zA-Z0-9]+:[a-zA-Z0-9]{32,40}[^\s]*)")

bot = telebot.TeleBot(BOT_TOKEN)
_bot_started = False


def is_authorized(message):
    return message.from_user and message.from_user.id == ALLOWED_USER_ID


def main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("Start Torrent Download"),
        types.KeyboardButton("Get Torrents Status"),
        types.KeyboardButton("Delete Torrent"),
        types.KeyboardButton("Get Device Info"),
    )
    return markup


def format_device_info():
    try:
        bat = get_battery()
        storage_list = get_storage()
        ram = get_ram()

        lines = ["📱 *Device Status & Info*\n"]
        
        # Battery
        lines.append("🔋 *Battery:*")
        lines.append(f"• Level: *{bat.get('level')}%* ({bat.get('status')})")
        lines.append(f"• Temp: `{bat.get('temp_c')}°C` | Voltage: `{bat.get('voltage_v')}V`")
        lines.append(f"• Health: {bat.get('health')}\n")

        # Storage
        lines.append("💾 *Storage:*")
        if storage_list:
            for vol in storage_list:
                lines.append(f"• *{vol.get('name')}*: {vol.get('total_gb')} GB total / {vol.get('used_gb')} GB used ({vol.get('percent')}%)")
        else:
            lines.append("• No storage volumes detected")
        lines.append("")

        # RAM
        lines.append("🧠 *RAM:*")
        lines.append(f"• Total: `{ram.get('total_gb')} GB` | Used: `{ram.get('used_gb')} GB` ({ram.get('percent')}%)")
        lines.append(f"• Available: `{ram.get('avail_gb')} GB`")

        return "\n".join(lines)
    except Exception as e:
        return f"❌ Failed to fetch device info:\n`{str(e)}`"


def format_torrent_status():
    try:
        proc = subprocess.run(
            [TRANSMISSION_REMOTE, "-l"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if proc.returncode != 0:
            return f"❌ Transmission Error:\n`{proc.stderr.strip() or 'Daemon not running'}`"

        lines = proc.stdout.strip().splitlines()
        if len(lines) <= 2:
            return "📭 *Torrent Queue Empty*\nNo active or queued downloads."

        formatted = ["📥 *Active Torrents:*"]
        # Skip header (index 0) and summary footer (last line)
        for line in lines[1:-1]:
            parts = line.split()
            if len(parts) >= 9:
                tid = parts[0].replace("*", "")
                done = parts[1]
                eta = f"{parts[4]} {parts[5]}" if parts[4] not in ("Done", "Unknown") else parts[4]
                down = parts[-4]
                status = parts[-2]
                name = " ".join(parts[8:]) if len(parts) > 9 else parts[-1]
                if len(formatted) > 1:
                    formatted.append("")
                formatted.append(
                    f"• *[{tid}]* `{name}`\n"
                    f"  Progress: *{done}* | Speed: `{down} KB/s` | ETA: `{eta}` ({status})"
                )

        summary = lines[-1].strip()
        formatted.append(f"\n`{summary}`")
        return "\n".join(formatted)
    except Exception as e:
        return f"❌ Failed to fetch status:\n`{str(e)}`"


def start_magnet_download(message):
    if not is_authorized(message):
        return

    text = (message.text or "").strip()

    # Allow user to cancel or switch command cleanly
    if text == "Get Torrents Status":
        bot.send_message(
            message.chat.id,
            format_torrent_status(),
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
        )
        return
    if text in ("Get Device Info", "/deviceinfo"):
        bot.send_message(
            message.chat.id,
            format_device_info(),
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
        )
        return
    if text in ("Delete Torrent", "/delete"):
        prompt_delete_torrent(message)
        return

    matches = MAGNET_REGEX.findall(text)
    if not matches:
        msg = bot.send_message(
            message.chat.id,
            "⚠️ Invalid magnet link. Please send a valid link starting with `magnet:?xt=...` (or tap a menu button below):",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
        )
        bot.register_next_step_handler(msg, start_magnet_download)
        return

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    for magnet in matches:
        res = subprocess.run(
            [TRANSMISSION_REMOTE, "-a", magnet, "-w", DOWNLOAD_DIR],
            capture_output=True,
            text=True,
        )
        if res.returncode == 0:
            bot.send_message(
                message.chat.id,
                f"✅ *Download Process Started!*\nSaved to: `{DOWNLOAD_DIR}`",
                parse_mode="Markdown",
                reply_markup=main_menu_keyboard(),
            )
        else:
            bot.send_message(
                message.chat.id,
                f"❌ *Failed to Start Download:*\n`{res.stderr.strip()}`",
                parse_mode="Markdown",
                reply_markup=main_menu_keyboard(),
            )


def prompt_delete_torrent(message):
    if not is_authorized(message):
        return
    msg = bot.send_message(
        message.chat.id,
        "🗑️ Send the torrent ID to remove it and delete its downloaded files:",
        reply_markup=main_menu_keyboard(),
    )
    bot.register_next_step_handler(msg, delete_torrent)


def delete_torrent(message):
    if not is_authorized(message):
        return

    text = (message.text or "").strip()
    if text in ("Get Torrents Status", "/status"):
        handle_status(message)
        return
    if text in ("Start Torrent Download", "/download"):
        handle_download_prompt(message)
        return
    if text in ("Delete Torrent", "/delete"):
        prompt_delete_torrent(message)
        return
    if not re.fullmatch(r"[1-9]\d*", text):
        msg = bot.send_message(
            message.chat.id,
            "⚠️ Enter a positive numeric torrent ID, or use a menu button to cancel.",
            reply_markup=main_menu_keyboard(),
        )
        bot.register_next_step_handler(msg, delete_torrent)
        return

    try:
        result = subprocess.run(
            [TRANSMISSION_REMOTE, "-t", text, "--remove-and-delete"],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except FileNotFoundError:
        response = "❌ transmission-remote binary not found."
    except subprocess.TimeoutExpired:
        response = "❌ Timed out while removing the torrent."
    else:
        if result.returncode == 0:
            response = f"✅ Torrent {text} and its downloaded files were removed."
        else:
            error = result.stderr.strip() or result.stdout.strip() or "Transmission did not remove the torrent."
            response = f"❌ Failed to remove torrent {text}: {error}"

    bot.send_message(
        message.chat.id,
        response,
        reply_markup=main_menu_keyboard(),
    )


@bot.message_handler(commands=["start", "help"])
def handle_start(message):
    if not is_authorized(message):
        return

    # Register native Telegram "/" commands menu
    bot.set_my_commands([
        types.BotCommand("download", "Start torrent download via magnet link"),
        types.BotCommand("status", "Get current torrents status"),
        types.BotCommand("delete", "Remove a torrent and its downloaded files"),
        types.BotCommand("deviceinfo", "Get battery, storage, and RAM device info"),
    ])

    bot.send_message(
        message.chat.id,
        "🤖 *Patoli Moto Hub Bot Ready*\nChoose a command below or paste a magnet link directly:",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


@bot.message_handler(commands=["download"])
@bot.message_handler(func=lambda m: m.text == "Start Torrent Download")
def handle_download_prompt(message):
    if not is_authorized(message):
        return
    msg = bot.send_message(
        message.chat.id,
        "🧲 Please send the *magnet link* now:",
        parse_mode="Markdown",
    )
    bot.register_next_step_handler(msg, start_magnet_download)


@bot.message_handler(commands=["status"])
@bot.message_handler(func=lambda m: m.text == "Get Torrents Status")
def handle_status(message):
    if not is_authorized(message):
        return
    bot.send_message(
        message.chat.id,
        format_torrent_status(),
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


@bot.message_handler(commands=["deviceinfo"])
@bot.message_handler(func=lambda m: m.text == "Get Device Info")
def handle_device_info(message):
    if not is_authorized(message):
        return
    bot.send_message(
        message.chat.id,
        format_device_info(),
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


@bot.message_handler(commands=["delete"])
@bot.message_handler(func=lambda m: m.text == "Delete Torrent")
def handle_delete_prompt(message):
    prompt_delete_torrent(message)


# Fallback: if you paste a magnet link directly without pressing Command 1 first
@bot.message_handler(func=lambda m: bool(m.text and MAGNET_REGEX.search(m.text)))
def handle_direct_magnet(message):
    start_magnet_download(message)


def _run_polling():
    bot.infinity_polling(timeout=60, long_polling_timeout=60)


def init_bot():
    global _bot_started
    if not _bot_started:
        _bot_started = True
        thread = threading.Thread(target=_run_polling, daemon=True)
        thread.start()


@bp.get("/status")
def bot_api_status():
    return jsonify({"running": _bot_started})


# Automatically launch the Telegram listener when app.py imports this module
init_bot()
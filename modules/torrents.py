import os
import re
import subprocess
from flask import Blueprint, jsonify, send_file

bp = Blueprint("torrents", __name__, url_prefix="/api/torrents")

TRANSMISSION_REMOTE = "/data/data/com.termux/files/usr/bin/transmission-remote"
TORRENT_ROW_PATTERN = re.compile(
    r"^\s*(\d+)\*?\s+(\S+)\s+(None|[\d.]+\s+\S+)\s+"
    r"(Done|Unknown|N/A|\d+:\d{2}:\d{2}|[\d.]+\s+\S+)\s+"
    r"(\S+)\s+(\S+)\s+(\S+)\s+(.+?)\s{2,}(.+?)\s*$"
)
TORRENT_FILE_PATTERN = re.compile(
    r"^\s*(\d+):\s+([\d.]+)%\s+\S+\s+(Yes|No)\s+(.{9})  (.+?)\s*$"
)


class TransmissionCommandError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code


def run_transmission(arguments):
    try:
        proc = subprocess.run(
            [TRANSMISSION_REMOTE, *arguments],
            capture_output=True,
            text=True,
            timeout=5
        )
    except FileNotFoundError as exc:
        raise TransmissionCommandError("transmission-remote binary not found", 500) from exc
    except subprocess.TimeoutExpired as exc:
        raise TransmissionCommandError("Timed out while querying Transmission", 504) from exc

    if proc.returncode != 0:
        raise TransmissionCommandError(
            proc.stderr.strip() or "Unable to query Transmission",
            502
        )
    return proc.stdout


def parse_torrent_list(output):
    lines = output.splitlines()
    if len(lines) < 2:
        return []

    items = []
    for line in lines[1:]:
        match = TORRENT_ROW_PATTERN.match(line)
        if not match:
            continue

        torrent_id, done, have, eta, up, down, ratio, status, name = match.groups()
        items.append({
            "id": torrent_id,
            "done": done,
            "have": have,
            "eta": eta,
            "up": up,
            "down": down,
            "ratio": ratio,
            "status": status.strip(),
            "name": name,
        })
    return items


@bp.get("")
def get_torrents():
    try:
        proc = subprocess.run(
            [TRANSMISSION_REMOTE, "-l"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if proc.returncode != 0:
            return jsonify({
                "ok": False,
                "error": proc.stderr.strip() or "Transmission daemon not reachable",
                "raw": ""
            })

        raw_output = proc.stdout.strip()
        return jsonify({
            "ok": True,
            "raw": raw_output,
            "items": parse_torrent_list(raw_output)
        })
    except FileNotFoundError:
        return jsonify({"ok": False, "error": "transmission-remote binary not found", "raw": ""})
    except subprocess.TimeoutExpired:
        return jsonify({"ok": False, "error": "Timed out while querying Transmission", "raw": ""})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "raw": ""})


def parse_torrent_files(output):
    files = []
    for line in output.splitlines():
        match = TORRENT_FILE_PATTERN.match(line)
        if not match:
            continue

        file_index, done, wanted, size, name = match.groups()
        files.append({
            "id": int(file_index),
            "done": float(done),
            "wanted": wanted == "Yes",
            "size": size.strip(),
            "name": name,
        })
    return files


def resolve_download_path(location, torrent_name, file_name, is_multi_file):
    relative_parts = file_name.replace("\\", "/").split("/")
    if os.path.isabs(file_name) or any(part in ("", ".", "..") for part in relative_parts):
        return None

    location = os.path.realpath(location)
    if is_multi_file:
        if not torrent_name or os.path.basename(torrent_name) != torrent_name:
            return None
        candidates = []
        if relative_parts[0] == torrent_name:
            candidates.append(os.path.join(location, *relative_parts))
            candidates.append(os.path.join(location, *relative_parts[1:]))
        candidates.extend((
            os.path.join(location, torrent_name, *relative_parts),
            os.path.join(location, *relative_parts),
        ))
    else:
        candidates = [os.path.join(location, *relative_parts)]

    for candidate in candidates:
        candidate = os.path.realpath(candidate)
        try:
            if os.path.commonpath([location, candidate]) != location:
                continue
        except ValueError:
            continue
        if os.path.isfile(candidate):
            return candidate
    return None


def get_completed_files(torrent_id):
    info = run_transmission(["-t", str(torrent_id), "-i"])
    name_match = re.search(r"^\s*Name:\s*(.*?)\s*$", info, re.MULTILINE)
    location_match = re.search(r"^\s*Location:\s*(.*?)\s*$", info, re.MULTILINE)
    if not name_match or not location_match:
        raise TransmissionCommandError("Transmission did not return the torrent's file location", 404)

    files_output = run_transmission(["-t", str(torrent_id), "-if"])
    file_entries = parse_torrent_files(files_output)
    completed_files = []
    for entry in file_entries:
        if not entry["wanted"] or entry["done"] < 100:
            continue
        path = resolve_download_path(
            location_match.group(1),
            name_match.group(1),
            entry["name"],
            len(file_entries) > 1
        )
        if path:
            entry["path"] = path
            completed_files.append(entry)
    return completed_files


@bp.get("/<int:torrent_id>/files")
def list_completed_files(torrent_id):
    try:
        files = get_completed_files(torrent_id)
    except TransmissionCommandError as exc:
        return jsonify({"ok": False, "error": str(exc)}), exc.status_code

    return jsonify({
        "ok": True,
        "files": [
            {
                "id": item["id"],
                "name": item["name"],
                "size": item["size"],
                "url": f"/api/torrents/{torrent_id}/files/{item['id']}"
            }
            for item in files
        ]
    })


@bp.get("/<int:torrent_id>/files/<int:file_index>")
def download_completed_file(torrent_id, file_index):
    try:
        files = get_completed_files(torrent_id)
    except TransmissionCommandError as exc:
        return jsonify({"error": str(exc)}), exc.status_code

    file_entry = next((item for item in files if item["id"] == file_index), None)
    if file_entry is None:
        return jsonify({"error": "This completed file is not available on the phone"}), 404

    return send_file(
        file_entry["path"],
        as_attachment=True,
        download_name=os.path.basename(file_entry["name"]),
    )
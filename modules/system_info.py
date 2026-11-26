import os
import shutil
import subprocess
import socket
from flask import Blueprint, jsonify

bp = Blueprint("system_info", __name__, url_prefix="/api/system")

def _read_file(path, default="N/A"):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except Exception:
        return default

def _getprop(prop, default="Unknown"):
    try:
        out = subprocess.check_output(["getprop", prop], text=True, timeout=2).strip()
        return out if out else default
    except Exception:
        return default

def get_ram():
    mem = {}
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 2:
                    mem[parts[0].rstrip(":")] = int(parts[1])  # kB
        total_gb = round(mem.get("MemTotal", 0) / 1048576, 2)
        avail_gb = round(mem.get("MemAvailable", 0) / 1048576, 2)
        used_gb = round(total_gb - avail_gb, 2)
        pct = round((used_gb / total_gb) * 100, 1) if total_gb else 0
        return {"total_gb": total_gb, "used_gb": used_gb, "avail_gb": avail_gb, "percent": pct}
    except Exception:
        return {"total_gb": 0, "used_gb": 0, "avail_gb": 0, "percent": 0}

def get_storage():
    volumes = []
    targets = [
        ("Internal Storage", "/data/media/0"),
        ("System Data", "/data"),
    ]
    # Auto-detect external MicroSD card if mounted under /storage/
    if os.path.exists("/storage"):
        for entry in os.listdir("/storage"):
            if entry not in ("emulated", "self") and "-" in entry:
                targets.append((f"SD Card ({entry})", f"/storage/{entry}"))

    for label, path in targets:
        if os.path.exists(path):
            try:
                usage = shutil.disk_usage(path)
                total_gb = round(usage.total / (1024**3), 1)
                used_gb = round(usage.used / (1024**3), 1)
                free_gb = round(usage.free / (1024**3), 1)
                pct = round((usage.used / usage.total) * 100, 1) if usage.total else 0
                volumes.append({
                    "name": label,
                    "total_gb": total_gb,
                    "used_gb": used_gb,
                    "free_gb": free_gb,
                    "percent": pct
                })
            except Exception:
                pass
    return volumes

def get_battery():
    base = "/sys/class/power_supply/battery"
    level = _read_file(f"{base}/capacity", "0")
    status = _read_file(f"{base}/status", "Unknown")
    raw_temp = _read_file(f"{base}/temp", "0")
    temp_c = round(int(raw_temp) / 10.0, 1) if raw_temp.lstrip("-").isdigit() else "N/A"
    raw_volt = _read_file(f"{base}/voltage_now", "0")
    voltage_v = round(int(raw_volt) / 1_000_000.0, 2) if raw_volt.isdigit() else "N/A"
    health = _read_file(f"{base}/health", "Good")

    return {
        "level": level,
        "status": status,
        "is_charging": status == "Charging",
        "temp_c": temp_c,
        "voltage_v": voltage_v,
        "health": health
    }

def get_phone_ip():
    ipv4 = "N/A"
    ipv6 = "N/A"
    try:
        # Determine active local IPv4 via socket connection test
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("10.255.255.255", 1))
            ipv4 = s.getsockname()[0]
        except Exception:
            pass
        finally:
            s.close()

        # Enumerate host addresses for dual-stack support & fallback
        try:
            hostname = socket.gethostname()
            addr_info = socket.getaddrinfo(hostname, None)
            ipv4_candidates = []
            ipv6_candidates = []
            for fam, _, _, _, sockaddr in addr_info:
                ip = sockaddr[0]
                if fam == socket.AF_INET:
                    if not ip.startswith("127."):
                        ipv4_candidates.append(ip)
                elif fam == socket.AF_INET6:
                    if not ip.startswith("::1"):
                        ipv6_candidates.append(ip.split('%')[0])

            if ipv4 == "N/A" and ipv4_candidates:
                ipv4 = ipv4_candidates[0]
            if ipv6_candidates:
                ipv6 = ipv6_candidates[0]
        except Exception:
            pass
    except Exception:
        pass

    return {
        "ipv4": ipv4 if ipv4 else "N/A",
        "ipv6": ipv6 if ipv6 else "N/A"
    }

def get_device():
    uptime_sec = 0
    try:
        uptime_sec = float(_read_file("/proc/uptime", "0").split()[0])
    except Exception:
        pass
    hours = int(uptime_sec // 3600)
    mins = int((uptime_sec % 3600) // 60)

    return {
        "model": _getprop("ro.product.model", "Android Device"),
        "manufacturer": _getprop("ro.product.manufacturer", "Unknown"),
        "android_version": _getprop("ro.build.version.release", "12"),
        "kernel": os.uname().release.split("-")[0],
        "uptime": f"{hours}h {mins}m",
        "phone_ip": get_phone_ip()
    }

@bp.get("")
def system_overview():
    return jsonify({
        "ram": get_ram(),
        "storage": get_storage(),
        "battery": get_battery(),
        "device": get_device()
    })

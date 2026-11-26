import os
import subprocess
import socket
import re
import time
from flask import Blueprint, jsonify

bp = Blueprint("wifi", __name__, url_prefix="/api/wifi")

def _read_file(path, default="N/A"):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except Exception:
        return default

def _run_cmd(cmd_list, timeout=2):
    try:
        res = subprocess.run(cmd_list, capture_output=True, text=True, timeout=timeout)
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        pass
    return ""

def get_wifi_status():
    wifi_data = {
        "connected": False,
        "ssid": "Disconnected",
        "rssi": "N/A",
        "ip_address": "N/A",
        "gateway": "N/A",
        "frequency_band": "N/A",
        "link_speed": "N/A",
        "connection_duration": "0m"
    }

    try:
        dumpsys = _run_cmd(["dumpsys", "wifi"])
        if dumpsys:
            ssid_match = re.search(r'SSID:\s*"?([^,\"\n]+)"?', dumpsys)
            if ssid_match and ssid_match.group(1).strip() and "<unknown ssid>" not in ssid_match.group(1).lower():
                wifi_data["connected"] = True
                wifi_data["ssid"] = ssid_match.group(1).strip()

            rssi_match = re.search(r'Rssi:\s*(-?\d+)', dumpsys)
            if rssi_match:
                wifi_data["rssi"] = f"{rssi_match.group(1)} dBm"

            link_speed_match = re.search(r'Link speed:\s*(\d+\s*Mbps)', dumpsys, re.IGNORECASE)
            if link_speed_match:
                wifi_data["link_speed"] = link_speed_match.group(1)

            freq_match = re.search(r'Frequency:\s*(\d+\s*MHz)', dumpsys, re.IGNORECASE)
            if freq_match:
                freq_val = int(re.search(r'\d+', freq_match.group(1)).group())
                wifi_data["frequency_band"] = "5 GHz" if freq_val > 4900 else "2.4 GHz"

        ip_addr = "N/A"
        gateway = "N/A"

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_addr = s.getsockname()[0]
            s.close()
        except Exception:
            pass

        if ip_addr != "N/A":
            wifi_data["connected"] = True
            wifi_data["ip_address"] = ip_addr
            if wifi_data["ssid"] == "Disconnected":
                wifi_data["ssid"] = "Connected Wi-Fi"

        route_out = _run_cmd(["ip", "route"])
        if not route_out:
            route_out = _run_cmd(["route", "-n"])

        gw_match = re.search(r'default via ([^\s]+)', route_out)
        if gw_match:
            gateway = gw_match.group(1)
        elif "default" in route_out:
            parts = route_out.split()
            for i, p in enumerate(parts):
                if p == "via" and i + 1 < len(parts):
                    gateway = parts[i + 1]
                    break
        wifi_data["gateway"] = gateway

        for wlan_interface in ("wlan0", "wlan1"):
            speed = _read_file(f"/sys/class/net/{wlan_interface}/speed", "")
            if speed and speed.isdigit():
                wifi_data["link_speed"] = f"{speed} Mbps"
                break

        if wifi_data["connected"]:
            uptime = _read_file("/proc/uptime", "")
            try:
                uptime_seconds = float(uptime.split()[0])
                hours = int(uptime_seconds // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                wifi_data["connection_duration"] = f"{hours}h {minutes}m" if hours else f"{minutes}m"
            except Exception:
                wifi_data["connection_duration"] = "Active"
    except Exception:
        pass

    return wifi_data

def get_connected_devices():
    devices = []
    seen_ips = set()

    # 1. Parse /proc/net/arp
    if os.path.exists("/proc/net/arp"):
        try:
            content = _read_file("/proc/net/arp")
            lines = content.splitlines()
            for line in lines[1:]: # Skip header
                parts = line.split()
                if len(parts) >= 6:
                    ip = parts[0]
                    mac = parts[3]
                    if ip != "0.0.0.0" and mac != "00:00:00:00:00:00" and ip not in seen_ips:
                        seen_ips.add(ip)
                        # Try reverse DNS or set generic hostname
                        hostname = f"Device-{ip.split('.')[-1]}"
                        try:
                            hostname = socket.gethostbyaddr(ip)[0]
                        except Exception:
                            pass
                        devices.append({
                            "hostname": hostname,
                            "ip_address": ip,
                            "mac_address": mac,
                            "connection_duration": "Active"
                        })
        except Exception:
            pass

    # 2. Parse ip neigh
    neigh_out = _run_cmd(["ip", "neigh"])
    if neigh_out:
        for line in neigh_out.splitlines():
            parts = line.split()
            if len(parts) >= 5:
                ip = parts[0]
                mac = "unknown"
                for i, p in enumerate(parts):
                    if p == "lladdr" and i + 1 < len(parts):
                        mac = parts[i + 1]
                        break
                if ip not in seen_ips and mac != "unknown":
                    seen_ips.add(ip)
                    devices.append({
                        "hostname": f"Peer-{ip.split('.')[-1]}",
                        "ip_address": ip,
                        "mac_address": mac,
                        "connection_duration": "Active"
                    })

    return devices

@bp.get("")
def wifi_overview():
    return jsonify({
        "wifi": get_wifi_status(),
        "devices": get_connected_devices()
    })

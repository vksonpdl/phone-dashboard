# API Contract: System Info & Phone IP Endpoint

**Feature**: Enhance Device Info with Phone IP (`004-deviceinfo-phone-ip`)

## Endpoint

`GET /api/system`

### Description
Returns system overview data including RAM, storage, battery, and enhanced device details containing the local network **Phone IP** (both IPv4 and IPv6 when available, with Wi-Fi interface precedence).

### Response Headers
- `Content-Type: application/json`

### Success Response (200 OK)
```json
{
  "ram": {
    "total_gb": 3.76,
    "used_gb": 1.45,
    "avail_gb": 2.31,
    "percent": 38.6
  },
  "storage": [
    {
      "name": "Internal Storage",
      "total_gb": 110.0,
      "used_gb": 45.2,
      "free_gb": 64.8,
      "percent": 41.1
    }
  ],
  "battery": {
    "level": "85",
    "status": "Discharging",
    "is_charging": false,
    "temp_c": 31.2,
    "voltage_v": 3.85,
    "health": "Good"
  },
  "device": {
    "model": "Pixel 6",
    "manufacturer": "Google",
    "android_version": "13",
    "kernel": "5.10.43",
    "uptime": "14h 32m",
    "phone_ip": {
      "ipv4": "192.168.1.105",
      "ipv6": "2001:db8::5678"
    }
  }
}
```

### Offline / Fallback Response (200 OK)
```json
{
  "ram": { ... },
  "storage": [ ... ],
  "battery": { ... },
  "device": {
    "model": "Pixel 6",
    "manufacturer": "Google",
    "android_version": "13",
    "kernel": "5.10.43",
    "uptime": "14h 32m",
    "phone_ip": {
      "ipv4": "N/A",
      "ipv6": "N/A"
    }
  }
}
```

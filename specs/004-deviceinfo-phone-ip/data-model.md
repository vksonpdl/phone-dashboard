# Data Model: Phone IP in Device Info

**Feature**: Enhance Device Info with Phone IP (`004-deviceinfo-phone-ip`)

## Entities

### Device Info Response (Extended)
The existing `device` entity in the system overview API is enhanced to include the `phone_ip` attribute.

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `model` | string | Device model name | `"Android Device"` |
| `manufacturer` | string | Device manufacturer | `"Google"` |
| `android_version` | string | Android OS release version | `"12"` |
| `kernel` | string | Linux kernel version | `"4.19"` |
| `uptime` | string | System uptime duration | `"5h 12m"` |
| `phone_ip` | object / string | Active local network IP address(es) supporting both IPv4 and IPv6 | `{"ipv4": "192.168.1.15", "ipv6": "fe80::1%wlan0"}` (or `"192.168.1.15 / fe80::1"`) |

## API Response Payload Structure

The endpoint `GET /api/system` returns JSON including the enhanced `device` object:

```json
{
  "ram": { ... },
  "storage": [ ... ],
  "battery": { ... },
  "device": {
    "model": "Android Device",
    "manufacturer": "Unknown",
    "android_version": "12",
    "kernel": "5.4.0",
    "uptime": "2h 15m",
    "phone_ip": {
      "ipv4": "192.168.1.15",
      "ipv6": "fe80::1%wlan0"
    }
  }
}
```

When offline / airplane mode / restricted:
```json
{
  "ram": { ... },
  "storage": [ ... ],
  "battery": { ... },
  "device": {
    "model": "Android Device",
    "manufacturer": "Unknown",
    "android_version": "12",
    "kernel": "5.4.0",
    "uptime": "2h 15m",
    "phone_ip": {
      "ipv4": "N/A",
      "ipv6": "N/A"
    }
  }
}
```

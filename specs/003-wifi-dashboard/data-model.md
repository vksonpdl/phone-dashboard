# Data Model: Wi-Fi Dashboard

**Feature**: Expose Wi-Fi Dashboard in Patoli MotoHub Dashboard (`003-wifi-dashboard`)

## Entities

### 1. Wi-Fi Network
Represents the state and connection parameters of the mobile device's active wireless connection.

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `connected` | boolean | Indicates whether the device has an active Wi-Fi connection | `true` |
| `ssid` | string | Network Name / SSID | `"HomeNetwork_5G"` |
| `rssi` | string / integer | Signal strength in dBm or signal level descriptor | `"-52 dBm"` (or `"Good"`) |
| `ip_address` | string | Local IP address assigned to the mobile device | `"192.168.1.145"` |
| `gateway` | string | Network gateway IP address | `"192.168.1.1"` |
| `frequency_band` | string | Operating frequency band | `"5 GHz"` |
| `link_speed` | string | Current negotiated link speed | `433 Mbps` |
| `connection_duration` | string | Duration of the active connection session | `"1h 24m"` |

### 2. Connected Device
Represents a peer device discovered on the local network via ARP / neighbor tables.

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `hostname` | string | Resolved or reported device name / hostname | `"LivingRoom-TV"` |
| `ip_address` | string | Peer device IP address | `"192.168.1.110"` |
| `mac_address` | string | Hardware MAC address | `"aa:bb:cc:dd:ee:ff"` |
| `connection_duration` | string | Estimated time connected or session duration | `"2h 15m"` (or `"Active"`) |

## API Response Payload Structure

The endpoint `GET /api/wifi` returns JSON matching this structure:

```json
{
  "wifi": {
    "connected": true,
    "ssid": "HomeNetwork_5G",
    "rssi": "-52 dBm",
    "ip_address": "192.168.1.145",
    "gateway": "192.168.1.1",
    "frequency_band": "5 GHz",
    "link_speed": "433 Mbps",
    "connection_duration": "1h 24m"
  },
  "devices": [
    {
      "hostname": "LivingRoom-TV",
      "ip_address": "192.168.1.110",
      "mac_address": "aa:bb:cc:dd:ee:ff",
      "connection_duration": "Active"
    }
  ]
}
```

When disconnected:
```json
{
  "wifi": {
    "connected": false,
    "ssid": "Disconnected",
    "rssi": "N/A",
    "ip_address": "N/A",
    "gateway": "N/A",
    "frequency_band": "N/A",
    "link_speed": "N/A",
    "connection_duration": "0m"
  },
  "devices": []
}
```

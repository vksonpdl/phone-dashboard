# API Contract: Wi-Fi Dashboard Endpoint

**Feature**: Expose Wi-Fi Dashboard in Patoli MotoHub Dashboard (`003-wifi-dashboard`)

## Endpoint

`GET /api/wifi`

### Description
Returns JSON containing active Wi-Fi connection metrics (including SSID, RSSI, IP, gateway, frequency band, link speed, and connection duration) as well as a list of connected peer devices on the local network.

### Response Headers
- `Content-Type: application/json`

### Success Response (200 OK)
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

### Disconnected State Response (200 OK)
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

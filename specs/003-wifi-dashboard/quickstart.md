# Quickstart Validation Guide: Wi-Fi Dashboard

**Feature**: Expose Wi-Fi Dashboard in Patoli MotoHub Dashboard (`003-wifi-dashboard`)

## Overview
This guide outlines the steps to validate the Wi-Fi Dashboard feature end-to-end.

## Prerequisites
- Python 3.x installed with Flask library.
- Repository cloned locally.

## Setup & Run Instructions

1. **Start the Flask Application**:
   ```bash
   python app.py
   ```
2. **Access the Dashboard**:
   Open browser at `http://127.0.0.1:5000/`.

3. **Verify API Endpoint**:
   ```bash
   curl http://127.0.0.1:5000/api/wifi
   ```
   *Expected Outcome*: Returns JSON containing `wifi` object (with connected status, SSID, RSSI, IP, gateway, frequency band, link speed, and connection duration) and `devices` array.

4. **Verify UI Integration**:
   - Confirm **Wi-Fi Dashboard** tab is visible in the navigation bar.
   - Click the tab and verify metrics and connected devices render correctly.
   - Test auto-refresh dropdown and manual **Refresh Now** button (`↻`).

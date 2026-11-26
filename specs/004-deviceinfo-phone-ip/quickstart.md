# Quickstart Validation Guide: Enhance Device Info with Phone IP

**Feature**: Enhance Device Info with Phone IP (`004-deviceinfo-phone-ip`)

## Overview
This guide outlines the steps to validate the Phone IP enhancement in the system info endpoint end-to-end.

## Prerequisites
- Python 3.x installed with Flask.
- Repository cloned locally.

## Setup & Run Instructions

1. **Start the Flask Application**:
   ```bash
   python app.py
   ```
2. **Access the API Endpoint**:
   ```bash
   curl http://127.0.0.1:5000/api/system
   ```
   *Expected Outcome*: Returns JSON containing the `device` object with `phone_ip` (including `ipv4` and `ipv6` fields) alongside `ram`, `storage`, and `battery`.

3. **Verify Offline / Fallback Behavior**:
   - Disconnect network / enable airplane mode or simulate network exception.
   - Query `http://127.0.0.1:5000/api/system`.
   - *Expected Outcome*: Endpoint returns `200 OK` successfully without error, with `phone_ip` falling back to `"N/A"` or `"Unavailable"`.

4. **Run Automated Unit Tests**:
   ```bash
   python -m unittest discover tests
   ```
   *Expected Outcome*: All existing and new unit tests pass successfully.

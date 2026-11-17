# Data Model: Telegram Device Info

The device info feature aggregates structured dictionaries provided by `modules.system_info`:

## 1. Battery Data Structure (`get_battery()`)
- `level` (str): Battery capacity percentage (e.g., `"85"`)
- `status` (str): Charging/discharging status (e.g., `"Charging"`, `"Discharging"`)
- `is_charging` (bool): True if status is Charging
- `temp_c` (float/str): Battery temperature in Celsius (e.g., `32.5`)
- `voltage_v` (float/str): Battery voltage in Volts (e.g., `3.85`)
- `health` (str): Battery health condition (e.g., `"Good"`)

## 2. Storage Data Structure (`get_storage()`)
List of volume dictionaries:
- `name` (str): Volume label (e.g., `"Internal Storage"`, `"System Data"`, `"SD Card (xxxx-xxxx)"`)
- `total_gb` (float): Total storage in GB
- `used_gb` (float): Used storage in GB
- `free_gb` (float): Free storage in GB
- `percent` (float): Usage percentage

## 3. RAM Data Structure (`get_ram()`)
- `total_gb` (float): Total RAM in GB
- `used_gb` (float): Used RAM in GB
- `avail_gb` (float): Available RAM in GB
- `percent` (float): RAM usage percentage

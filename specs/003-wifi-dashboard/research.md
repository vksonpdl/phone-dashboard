# Research: Wi-Fi Dashboard & Network Discovery

**Feature**: Expose Wi-Fi Dashboard in Patoli MotoHub Dashboard (`003-wifi-dashboard`)

## 1. Active Wi-Fi Connection Details Retrieval

- **Decision**: Use a combination of Android system commands (`dumpsys wifi`, `netcfg`, `ip route`, `iwconfig`) and Python standard socket/network interfaces wrapped in robust try/except blocks with simulation fallbacks for non-Android/desktop development environments.
- **Rationale**: Android devices typically provide detailed Wi-Fi state via `dumpsys wifi` or network configuration utilities. When running on non-Android or restricted environments (e.g., local Windows/Linux testing), the system should gracefully fall back to default/simulated connection metrics or local host network interfaces without crashing.
- **Alternatives Considered**:
  - *Third-party Python libraries (e.g., `wifi`, `scapy`)*: Rejected due to violation of the Minimalist Dependency Policy (Python stdlib + Flask only).
  - *Direct `/proc` reading only*: Insufficient for modern Android Wi-Fi state (SSID, RSSI, link speed).

## 2. Connected Network Devices Discovery

- **Decision**: Parse `/proc/net/arp` and query ARP table via `subprocess.run(["ip", "neigh"])` to discover peer devices connected to the local network.
- **Rationale**: `/proc/net/arp` is universally available on Linux/Android environments and contains the IP address, hardware address (MAC), and interface for connected local network neighbors. Supplementing with `ip neigh` provides robust coverage.
- **Alternatives Considered**:
  - *Active ping sweeping*: Too slow and can trigger network security alerts or consume excessive resources during frequent auto-refresh polling.
  - *External network discovery daemons*: Violates project constraints (no external binaries/dependencies).

## 3. Frontend Integration & Refresh Controls

- **Decision**: Add a new navigation tab (`<button class="tab-btn" data-tab="wifi">Wi-Fi Dashboard</button>`) and corresponding section panel (`<section id="tab-wifi" class="tab-panel">`) in `static/index.html`. Register a new async loader function in `TAB_LOADERS` in `index.html` that automatically executes during auto-refresh polling and manual "Refresh Now" clicks.
- **Rationale**: Directly aligns with existing architectural patterns used by "System Overview" and "Torrent Status" tabs, preserving polling timer consistency and UX uniformity.

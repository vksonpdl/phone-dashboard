# Feature Specification: Expose Wi-Fi Dashboard in Patoli MotoHub Dashboard

**Feature Branch**: `003-wifi-dashboard`

**Created**: 2026-11-20

**Status**: Draft

**Input**: User description: "Fetch GitHub issue https://github.com/vksonpdl/phone-dashboard/issues/3 using the GitHub MCP server (including all comments and labels). Use the requirements and acceptance criteria from that issue to generate spec.md."

## Clarifications

### Session 2026-11-20
- Q: Can active Wi-Fi connection details include connection duration? → A: Yes, include connection duration for the active Wi-Fi connection as well.
- Q: Can connected device info return the duration of active connection of the other connected devices as well? → A: Return the active device’s connection duration and an observed duration for each discovered peer device.
- Q: What should the dashboard treat as a “currently connected” device when the phone’s local network table may contain stale entries? → A: Use the phone’s network tables, exclude entries explicitly marked unreachable, and do not show mock devices.
- Q: When the phone cannot resolve a peer’s real hostname, should the API avoid fabricated `Device-*` names and return `Unknown` while keeping the device’s IP and MAC? → A: Yes, show `Unknown` and retain IP/MAC; use a resolved hostname only when available.
- Q: Should peer duration mean time since the dashboard first detected a device, rather than its actual Wi-Fi association time? → A: Show estimated time since first detection as “Observed for”; the timer starts when the dashboard first sees the device.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Active Wi-Fi Connection Details (Priority: P1)

As a dashboard user, I want to view detailed metrics and status of the mobile device's active Wi-Fi connection (including SSID, signal strength/RSSI, IP address, gateway, frequency band, link speed, and connection duration) so that I can monitor network connectivity and duration.

**Why this priority**: Provides the core value of the Wi-Fi Dashboard by surfacing immediate connectivity metrics for the host device.

**Independent Test**: Can be fully tested by navigating to the Wi-Fi Dashboard tab and verifying that active Wi-Fi connection parameters and duration are accurately rendered.

**Acceptance Scenarios**:

1. **Given** the mobile device is connected to a Wi-Fi network, **When** the user opens the Wi-Fi Dashboard tab, **Then** the network name (SSID), signal strength (RSSI/dBm), IP address, gateway, frequency band, link speed, and connection duration are displayed accurately.
2. **Given** the mobile device is not connected to any Wi-Fi network, **When** the user opens the Wi-Fi Dashboard tab, **Then** a graceful disconnected/empty state is displayed with clear messaging.

---

### User Story 2 - Discover and View Connected Network Devices (Priority: P2)

As a dashboard user, I want to see a list of other devices reported on the same Wi-Fi network along with their device identifiers (Hostname, IP Address, MAC Address) and estimated time since first detected so that I can audit network presence.

**Why this priority**: Extends the monitoring capabilities to peer devices on the local network.

**Independent Test**: Can be tested by verifying that peer devices are listed with their respective identifiers and estimated time since first detected.

**Acceptance Scenarios**:

1. **Given** other devices are reported on the same Wi-Fi network, **When** the Wi-Fi Dashboard loads or refreshes, **Then** a table or list displays each device's hostname/name, IP address, MAC address, and estimated time since first detected, labeled “Observed for.”
2. **Given** no peer devices are detected on the network, **When** the Wi-Fi Dashboard loads, **Then** an appropriate empty state message is shown for connected devices.

---

### User Story 3 - Dashboard Navigation & Refresh Controls Integration (Priority: P3)

As a dashboard user, I want the Wi-Fi Dashboard to be integrated into the main navigation bar and fully compatible with auto-polling and manual "Refresh Now" buttons so that my workflow remains uniform across all dashboard tabs.

**Why this priority**: Ensures cohesive UI navigation and consistent refresh behavior matching existing dashboard tabs.

**Independent Test**: Can be tested by toggling auto-refresh and clicking the manual refresh button to verify data updates correctly without resetting timers.

**Acceptance Scenarios**:

1. **Given** the Patoli MotoHub Dashboard is open, **When** the user looks at the navigation bar, **Then** a **Wi-Fi Dashboard** tab is visible and accessible.
2. **Given** the user is viewing the Wi-Fi Dashboard, **When** auto-refresh polling is active, **Then** active Wi-Fi details and connected device lists update automatically at the configured interval.
3. **Given** the user clicks the **Refresh Now** button, **When** data is reloaded, **Then** the latest Wi-Fi and connected device data is fetched immediately without disrupting active timers.

### Edge Cases

- What happens when the mobile device loses Wi-Fi connection while viewing the dashboard? (System displays fallback disconnected state gracefully).
- How does the system handle network discovery timeouts or restricted OS permissions? (System catches exceptions and returns empty lists or diagnostic messages without crashing).
- What happens when a disconnected device remains in the phone’s network table? (Entries explicitly marked unreachable are excluded; other stale entries may remain until the operating system updates its table).
- What happens during rapid sequential manual refreshes? (Duplicate requests are debounced or handled safely).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a navigation tab labeled **Wi-Fi Dashboard** in the existing Patoli MotoHub Dashboard navigation menu.
- **FR-002**: The system MUST retrieve and display baseline details of the mobile device's currently connected Wi-Fi network, including Network Name (SSID), Connection Status/Signal Strength (RSSI/dBm), IP Address & Gateway Details, Frequency Band, Link Speed, and Connection Duration (where available from the device/network layer).
- **FR-003**: The system MUST discover and list peer devices reported on the same Wi-Fi network, displaying their device identifiers (Hostname / Device Name, IP Address, and/or MAC Address) and an estimated duration since first detected, labeled “Observed for.”
- **FR-006**: The system MUST base the peer-device list on devices reported by the phone’s network tables, exclude entries explicitly marked unreachable, and never substitute simulated or mock devices when no peers are found.
- **FR-007**: When a peer’s real hostname cannot be resolved, the system MUST report `Unknown` as its hostname, retain the peer’s IP and MAC addresses, and MUST NOT generate a substitute hostname.
- **FR-004**: The system MUST integrate the Wi-Fi Dashboard with the existing Auto-refresh polling mechanism and support manual data reloads via the existing **Refresh Now** button without breaking or resetting active timers.
- **FR-005**: The system MUST handle disconnected or unavailable Wi-Fi states gracefully with clear user-friendly fallback messaging.

### Key Entities

- **Wi-Fi Network**: Represents the active wireless connection state, including SSID, RSSI, IP address, gateway, frequency band, link speed, and connection duration.
- **Connected Device**: Represents a peer device on the local network, including hostname/name, IP address, MAC address, and estimated time since first detected by the dashboard (“Observed for”), which is not the device’s actual Wi-Fi association duration.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can access the Wi-Fi Dashboard tab within 1 click from the main dashboard navigation bar.
- **SC-002**: Active Wi-Fi network details and connected device lists render successfully within 2 seconds of tab selection or manual refresh.
- **SC-003**: 100% of disconnected or unavailable network states display clear fallback messages without throwing unhandled exceptions.
- **SC-004**: Auto-refresh polling updates Wi-Fi metrics seamlessly at configured intervals without interrupting user interactions.

## Assumptions

- The host environment may provide access to wireless state and local network discovery mechanisms (such as system commands or network interface tables); unavailable data is reported as unavailable rather than replaced with simulated network devices.
- The existing Patoli MotoHub Dashboard front-end architecture supports modular tab extension and shared refresh controls.

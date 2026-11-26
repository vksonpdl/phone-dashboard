# Feature Specification: Enhance Device Info with Phone IP

**Feature Branch**: `004-deviceinfo-phone-ip`

**Created**: 2026-11-26

**Status**: Draft

**Input**: GitHub Issue #5: Enhance /deviceinfo with Phone IP

## Clarifications

### Session 2026-11-26
- Q: Should the Phone IP display the device's local network IP address, public internet IP address, or client request IP? → A: Local/private network IP address (Option A)
- Q: Should the system prioritize IPv4, IPv6, or both when multiple IP addresses are available? → A: Both IPv4 and IPv6 displayed simultaneously (Option C)
- Q: If multiple active network interfaces are available simultaneously, which interface should take precedence? → A: Wi-Fi preferred over Cellular / VPN (Option A)
- Q: What response format should the /deviceinfo endpoint return when providing the Phone IP alongside existing details? → A: Match existing JSON response structure

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Retrieve Phone IP in Device Info (Priority: P1)

As a user or support engineer running the `/deviceinfo` command, I want the result to include the device's IP address (**Phone IP**) alongside the existing device information, so that I can quickly verify network connectivity and identify the device on the network without running separate diagnostics.

**Why this priority**: Core value delivery of the feature requested in Issue #5, enabling immediate network verification and device identification.

**Independent Test**: Can be fully tested by invoking the `/deviceinfo` endpoint while connected to a network and verifying that the response contains all existing fields plus the correct `Phone IP`.

**Acceptance Scenarios**:

1. **Given** the device is connected to a network with an assigned IP address, **When** the user executes `/deviceinfo`, **Then** the output contains all existing device info fields plus the accurate `Phone IP`.
2. **Given** the device has no active network connection, **When** the user executes `/deviceinfo`, **Then** the command succeeds without error, displays all existing device info fields, and shows the fallback value (e.g., `N/A` or `Unavailable`) for `Phone IP`.

---

### Edge Cases

- **Offline / Airplane Mode**: Device has no active Wi-Fi or cellular connection -> Return fallback value (`N/A` / `Unavailable`).
- **Multiple Active Interfaces (Wi-Fi + Cellular + VPN)**: System applies a deterministic priority rule (e.g., Wi-Fi preferred over Cellular) rather than returning a random interface IP.
- **IPv4 vs. IPv6**: Device may have both IPv4 and IPv6 addresses assigned; selection preference is consistent.
- **Restricted Permissions**: If runtime/OS denies network interface enumeration, catch the exception and return the fallback value.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The `/deviceinfo` command MUST continue to return all existing device fields in their current structure and order (Backward Compatibility).
- **FR-002**: The system MUST resolve the device's active local/private non-loopback IP address at the time `/deviceinfo` is invoked.
- **FR-003**: The resolved IP address MUST be included in the `/deviceinfo` response clearly labeled as `Phone IP` (or corresponding structured key matching existing response conventions).
- **FR-004**: If the device has no active network interface, is in airplane mode, or lacks network state permissions, `/deviceinfo` MUST still succeed and display a fallback value (`Unavailable` or `N/A`) for `Phone IP`.
- **FR-005**: Loopback addresses (`127.0.0.1`, `::1`) MUST be excluded when selecting the active `Phone IP`.

### Key Entities *(include if feature involves data)*

- **DeviceInfo Response**: Structured JSON or text representation containing system properties (OS, uptime, memory, storage) and the newly added `Phone IP` field.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can retrieve device information including `Phone IP` with local execution latency under 50ms.
- **SC-002**: 100% of offline or restricted network edge cases return graceful fallback values without unhandled exceptions or crashes.
- **SC-003**: 100% backward compatibility maintained for all existing device info fields and unit test suites.

## Assumptions

- Target environment is Python 3.x Flask application running locally or on device.
- Standard socket or netifaces/psutil libraries available in Python runtime are used for local network interface inspection.
- Existing authorization and authentication checks on `/deviceinfo` apply unmodified.

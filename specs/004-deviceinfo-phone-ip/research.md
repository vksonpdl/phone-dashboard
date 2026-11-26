# Research: Phone IP Retrieval & Interface Prioritization

**Feature**: Enhance Device Info with Phone IP (`004-deviceinfo-phone-ip`)

## 1. Local Network IP Retrieval & Loopback Exclusion

- **Decision**: Use Python's standard `socket` library (`socket.getaddrinfo`, `socket.gethostname`, or `socket.connect`) combined with local network interface enumeration to extract active non-loopback IP addresses.
- **Rationale**: Python standard library `socket` operations execute locally in < 10ms without external dependencies or network calls, perfectly aligning with the < 50ms performance goal and Minimalist Dependency Policy. Loopback addresses (`127.0.0.1`, `::1`) and link-local addresses are explicitly filtered out.
- **Alternatives Considered**:
  - *Third-party `netifaces` or `psutil` libraries*: Rejected due to violation of the Minimalist Dependency Policy (no new third-party dependencies).

## 2. Dual-Stack Support (IPv4 and IPv6)

- **Decision**: Return both IPv4 and IPv6 addresses simultaneously as structured fields or formatted string values under `phone_ip` matching the clarification decision (Option C).
- **Rationale**: Accommodates modern networks utilizing dual-stack configurations without discarding either protocol.
- **Alternatives Considered**:
  - *IPv4 only*: Rejected per clarification decision to display both IPv4 and IPv6 when available.

## 3. Interface Priority (Wi-Fi Preferred over Cellular/VPN)

- **Decision**: Inspect network interface names or route tables (e.g., matching interface prefixes like `wlan`, `wifi`, `eth`, or parsing `ip route` / socket binding) to prioritize Wi-Fi interfaces over cellular (`rmnet`, `ccmni`, `cellular`) and VPN (`tun`, `tap`) interfaces.
- **Rationale**: Ensures deterministic, user-expected IP selection when multiple interfaces are active simultaneously.
- **Alternatives Considered**:
  - *Random order from `getaddrinfo`*: Rejected because it can return cellular or VPN IP unpredictably instead of local Wi-Fi.

## 4. Graceful Fallback on Offline / Airplane Mode

- **Decision**: Wrap all network interface inspection logic in a robust try/except block. When offline, in airplane mode, or encountering permission restrictions, return `"N/A"` or `"Unavailable"` without throwing exceptions or crashing.
- **Rationale**: Guarantees 100% reliability and robust error resilience as mandated by project constitution and requirements FR-004.

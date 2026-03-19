---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
System Code: NET
Full Name: FarmSense Network Architecture
Version: 2.0
---

> [!IMPORTANT]
> **MODULAR DAP (Drift Aversion Protocol)**
> **Module: D-DAP (Documentation)**
> 1. **Single Source of Truth**: This document is the authoritative reference for its subject matter.
> 2. **Synchronized Updates**: Any change to corresponding implementation MUST be reflected here immediately.
> 3. **AI Agent Compliance:** Agents MUST verify current implementation against this document before proposing changes.
> 4. **No Ghost Edits:** All significant modifications must be documented in the project's audit trail.

---

# NETWORK V2.0: FarmSense Network Architecture

## 1. Executive Summary

The FarmSense Network is a hierarchical multi-tier communication system connecting field sensors to cloud intelligence. The architecture uses purpose-built protocols at each tier: 900MHz CSS LoRa for sensor-to-PMT links (canopy penetration), 2.4GHz/LTE for PMT-to-DHU backhaul, 5GHz microwave for DHU-to-RSS aggregation, and fiber/internet for RSS-to-Cloud connectivity. The network is designed for agricultural environments with specific optimizations for canopy penetration, long-range rural links, and blackout survivability.

**Primary Role:** Multi-tier telemetry and command distribution
**Secondary Role:** RTK GNSS correction distribution
**Tertiary Role:** Byzantine fault-tolerant consensus network

---

## 2. Network Hierarchy

### 2.1 Tier Architecture

| Tier | Link | Technology | Range | Bandwidth |
|------|------|------------|-------|-----------|
| **Tier 0** | Sensor ↔ PMT | 900MHz CSS LoRa | 1km+ | 1.2kbps |
| **Tier 1** | PMT ↔ DHU | 2.4GHz LTU / LTE-M | 10km | 10Mbps / 1Mbps |
| **Tier 2** | DHU ↔ RSS | 5GHz PtP / Fiber | 20km | 500Mbps+ |
| **Tier 3** | RSS ↔ Cloud | Fiber / Internet | — | 1Gbps+ |

### 2.2 Protocol Stack by Tier

**Tier 0 (Sensor Field):**
- Physical: LoRa CSS @ 915MHz
- MAC: Custom TDMA
- Network: Star (PMT as hub)
- Transport: None (direct application)
- Application: CBOR-encoded sensor data
- Security: AES-128-CTR

**Tier 1 (Field Aggregation):**
- Physical: 2.4GHz ISM or LTE-M
- MAC: WiFi (LTU) or LTE PHY
- Network: IP (IPv4)
- Transport: QUIC
- Application: Protobuf
- Security: TLS 1.3 + mTLS

**Tier 2 (District Aggregation):**
- Physical: 5GHz microwave or fiber
- MAC: 802.11 (WiFi) or Ethernet
- Network: IP
- Transport: QUIC + custom PBFT
- Application: Protobuf
- Security: TLS 1.3 + cert pinning

**Tier 3 (Cloud Uplink):**
- Physical: Fiber or internet
- MAC: Ethernet
- Network: IP
- Transport: TLS over TCP
- Application: REST + gRPC
- Security: mTLS + JWT

---

## 3. Tier 0: LoRa Sensor Network

### 3.1 LoRa PHY Specifications

| Parameter | Specification |
|-----------|---------------|
| Frequency | 915MHz ISM band |
| Bandwidth | 125kHz |
| Spreading Factor | SF9-SF12 (adaptive) |
| Coding Rate | 4/5 |
| TX Power | +14 to +20dBm |
| Sensitivity | -148dBm @ SF9 |
| Link Budget | 160dB+ |

### 3.2 TDMA Schedule

**4-Hour Epoch (14,400 seconds):**

| Window | Duration | Assignment |
|--------|----------|------------|
| LRZB Beacon | 0-3s | 4 LRZB units transmit |
| LRZN Density | 3-15s | 12 LRZN units transmit |
| VFA Deep | 15-20s | 2 VFA units transmit |
| PFA Wellhead | 20-25s | 1 PFA unit transmits |
| Contention | 25-30s | Random access for alarms |
| Idle | 30-14,400s | All devices sleep |

**Duty Cycle:**
- Per device: <1% (FCC compliant)
- Total network: ~10% utilization
- Battery life: 4+ years

### 3.3 Canopy Penetration

| Crop Stage | 900MHz Loss | 2.4GHz Loss | Recommendation |
|------------|-------------|-------------|----------------|
| Bare soil | 0dB | 0dB | LoRa, 2.4GHz both work |
| Early growth | 3dB | 15dB | LoRa preferred |
| Full canopy | 6dB | 35dB+ | LoRa required |
| Dense corn | 10dB | 60dB+ | LoRa only option |

**Key Insight:** 2.4GHz fails completely in mature crops. LoRa is mandatory for sub-canopy sensor communication.

---

## 4. Tier 1: PMT-to-DHU Uplink

### 4.1 Primary: Ubiquiti LTU

| Parameter | Specification |
|-----------|---------------|
| Technology | Proprietary 2.4GHz TDMA |
| Bandwidth | 20MHz |
| Throughput | 10Mbps per PMT |
| Range | 10km+ (line of sight) |
| Latency | <5ms |
| Client Capacity | 100 per DHU sector |
| Antenna | 120° sector, 16dBi |

### 4.2 Fallback: LTE-M (Cat-M1)

| Parameter | Specification |
|-----------|---------------|
| Technology | 3GPP LTE Cat-M1 |
| Bands | B2, B4, B12 (North America) |
| Throughput | 1Mbps DL / 1Mbps UL |
| Range | Carrier-dependent |
| Latency | 50-100ms |
| Power | 20dBm output |
| Feature | eDRX for battery saving |

**Failover Logic:**
1. Attempt LTU connection (fast, high bandwidth)
2. If LTU fails for 5 minutes, activate LTE-M
3. If LTE-M fails for 10 minutes, enter "Black Box" mode
4. Store to SD card, retry every 15 minutes

---

## 5. Tier 2: DHU-to-RSS Aggregation

### 5.1 Primary: 5GHz Microwave PtP

| Parameter | Specification |
|-----------|---------------|
| Technology | 802.11ac/ax or proprietary |
| Frequency | 5.7GHz (UNII-3) |
| Bandwidth | 80MHz |
| Throughput | 500Mbps+ |
| Range | 20km+ (line of sight) |
| Latency | <1ms |
| Antenna | 34dBi dish (high gain) |

### 5.2 Alternative: Fiber Optic

| Parameter | Specification |
|-----------|---------------|
| Technology | Single-mode fiber |
| Bandwidth | 1Gbps+ (upgradable to 10Gbps) |
| Range | 20km without repeaters |
| Latency | <0.1ms |
| Reliability | Highest (no atmospheric effects) |

---

## 6. Tier 3: RSS-to-Cloud

### 6.1 Connection Methods

| Method | Bandwidth | Reliability | Use Case |
|--------|-----------|-------------|----------|
| Fiber | 1Gbps+ | Highest | Primary connection |
| Fixed Wireless | 100Mbps | High | Secondary/backup |
| LTE-A | 100Mbps | Medium | Emergency backup |
| Satellite | 50Mbps | Low | Last resort (Starlink) |

### 6.2 Zo Computer Integration

**API Endpoint:** `https://api.zo.computer/farmsense/v1/`

**Authentication:**
- mTLS with client certificates
- JWT for session management
- API key rotation every 90 days

**Data Flow:**
1. RSS aggregates from all DHUs
2. Encrypted bundle prepared (TLS 1.3)
3. Upload to Zo Computer
4. Acknowledgment with checksum
5. Local confirmation stored

---

## 7. RTK GNSS Distribution

### 7.1 RTK Base Station Network

| Level | Device | Role | Correction Range |
|-------|--------|------|------------------|
| DHU | ZED-F9P | District base | 10km radius |
| RSS | ZED-F9P | Regional backup | 20km radius |

### 7.2 Correction Distribution

**Method 1: 2.4GHz Broadcast (LTU)**
- RTCM 3.3 messages embedded in LTU frames
- All PMTs receive corrections automatically
- Latency: <1 second

**Method 2: NTRIP Server**
- Standard NTRIP v2.0 protocol
- Mount point: `DHU-CONEJOS-001_RTCM32`
- Accessible to external GNSS receivers

**RTK Performance:**
- Baseline accuracy: ±2cm horizontal
- Initialization: <30 seconds
- Availability: 99.9% (with multi-constellation)

---

## 8. AllianceChain PBFT Network

### 8.1 Consensus Topology

| Node Type | Count | Role |
|-----------|-------|------|
| Leader | 1 | Propose blocks (rotating) |
| Validator | 3+ | Validate and commit |
| Client | All DHUs | Submit transactions |

**Consensus Group:** 4+ DHUs per region
**Fault Tolerance:** f < n/3 (33% Byzantine)
**Block Time:** 60 seconds
**Finality:** Single-block confirmation

### 8.2 PBFT Message Flow

```
Client (DHU) → Leader: REQUEST
Leader → All Validators: PRE-PREPARE
Validator → All: PREPARE (2f+1 received)
Validator → All: COMMIT (2f+1 received)
All → Client: REPLY
```

**Network Requirements:**
- Latency: <100ms between nodes
- Bandwidth: 1Mbps per node (minimal)
- Reliability: 99% uptime (nodes can catch up)

---

## 9. Security Architecture

### 9.1 Encryption by Tier

| Tier | Encryption | Key Management |
|------|------------|----------------|
| 0 (LoRa) | AES-128-CTR | Per-device key (factory) |
| 1 (LTU) | AES-128-GCM (WiFi) | WPA3-Enterprise |
| 1 (LTE) | Snow 3G (3GPP) | SIM-based |
| 2 (PtP) | AES-256-GCM (TLS) | Certificate-based |
| 3 (Cloud) | AES-256-GCM (TLS 1.3) | mTLS + HSM |

### 9.2 Certificate Hierarchy

```
Root CA (bxthre3 internal)
├── Intermediate CA (per region)
│   ├── RSS certificates
│   │   └── DHU certificates
│   │       └── PMT certificates
│   └── Cloud service certificates
└── Device CA (manufacturing)
    ├── Factory device certs
    └── Field-programmable certs
```

### 9.3 Network Segmentation

| VLAN | Purpose | Devices |
|------|---------|---------|
| Management | SSH, monitoring | All infrastructure |
| Telemetry | Sensor data | PMT, DHU, RSS |
| PBFT | Consensus only | DHU inter-node |
| RTK | GNSS corrections | ZED-F9P outputs |
| Guest | Field tech access | Mobile devices |

---

## 10. Blackout Survivability

### 10.1 Degradation Modes

| Failure Level | Impact | Response |
|---------------|--------|----------|
| Cloud down | Analytics unavailable | DHU/RSS continue local ops |
| RSS down | Regional coordination lost | DHUs autonomous for 30 days |
| DHU down | District coordination lost | PMTs autonomous for 7 days |
| PMT down | Field coordination lost | Sensors autonomous for 30 days |

### 10.2 Data Preservation

| Device | Buffer | Retention | Action on Restore |
|--------|--------|-----------|-------------------|
| Sensor | RAM | 1 reading | Transmit immediately |
| PMT | SD card (32GB) | 7 days | Burst upload |
| DHU | SSD (128GB) | 30 days | Incremental sync |
| RSS | Tape (1PB) | 10 years | Archive complete |

---

## 11. Network Monitoring

### 11.1 Key Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| LoRa packet success | >95% | <90% |
| LTU link uptime | >99% | <95% |
| LTE failover events | <1/month | >5/month |
| PBFT consensus time | <1s | >5s |
| RTK correction age | <5s | >30s |
| End-to-end latency | <30s | >2min |

### 11.2 Alerting

**Severity Levels:**
- **P0 (Critical):** Complete link failure, consensus stall
- **P1 (High):** Degraded performance, failover active
- **P2 (Medium):** Elevated error rates, approaching limits
- **P3 (Low):** Informational, capacity planning

---

## 12. Integration & APIs

### 12.1 Network Health Query

```json
{
  "timestamp": "2026-03-19T14:30:00Z",
  "network_health": {
    "tier_0": {
      "lora_packets_24h": 89234,
      "packet_success_rate": 0.97,
      "avg_rssi": -72
    },
    "tier_1": {
      "ltu_links_active": 45,
      "ltu_links_degraded": 2,
      "lte_failover_active": 0
    },
    "tier_2": {
      "ptp_links_active": 7,
      "fiber_links_active": 0,
      "aggregate_throughput_mbps": 340
    },
    "tier_3": {
      "cloud_connected": true,
      "last_sync": "2026-03-19T14:29:00Z",
      "queue_depth": 12
    }
  },
  "pbft_status": {
    "consensus_active": true,
    "leader": "DHU-CONEJOS-001",
    "last_block": 1847293,
    "validator_count": 7
  }
}
```

---

## 13. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-03-01 | Initial architecture | Network |
| 1.5 | 2025-09-15 | Added LTE-M fallback | Comms |
| 2.0 | 2026-03-19 | Documentation standard | Documentation |

---

## 14. Related Documentation

- `PMT-SPEC.md` — LoRa hub implementation
- `DHU-SPEC.md` — Tier 1/2 gateway
- `RSS-SPEC.md` — Tier 2/3 aggregation
- `CLOUD-SPEC.md` — Cloud integration
- `MASTER_EVIDENCE_SPEC.md` — Security requirements

---

*Proprietary IP of bxthre3 inc. — Confidential*
*© 2026 bxthre3 inc. All rights reserved.*

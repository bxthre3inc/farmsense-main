---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
System Code: NET
Full Name: FarmSense Network Architecture
Version: 2.0
Category: System-Level Network Infrastructure
---

> [!IMPORTANT]
> **MODULAR DAP (Drift Aversion Protocol)**
> **Module: D-DAP (Documentation)**
> 
> 1. **Single Source of Truth**: This document is the authoritative reference for its subject matter.
> 2. **Synchronized Updates**: Any change to corresponding implementation MUST be reflected here immediately.
> 3. **AI Agent Compliance**: Agents MUST verify current implementation against this document before proposing changes.
> 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.
> 5. **EDIT RESTRICTION**: Changes require explicit approval from brodiblanco (Jeremy Beebe, CEO).
> 6. **ADDITIVE ONLY**: Specifications may only expand, never contract or summarize.

---

# NETWORK V2.0: FarmSense Network Architecture

## 1. Executive Summary

### 1.1 Role and Function

The FarmSense Network Architecture defines the **multi-layer communication fabric** that connects field sensors to district hubs to regional superstations to cloud infrastructure. This specification covers radio protocols, frequency bands, topology, security, and failover mechanisms across the entire telemetry chain.

**Primary Functions:**

1. **Sensor Aggregation**: Collect data from 20-34 sensors per field
2. **District Coordination**: Manage 100 fields per DHU
3. **Regional Synchronization**: Coordinate 10 DHUs per RSS
4. **Cloud Integration**: Upload to AWS for ML and compliance
5. **Failover Resilience**: Maintain operation during outages
6. **Security**: End-to-end encryption, zero-trust architecture

**Network Hierarchy:**

| Layer | Entity | Protocol | Range | Bandwidth |
|-------|--------|----------|-------|-----------|
| **L0** | Sensors → PMT | 900MHz CSS LoRa | 2km | 300bps |
| **L1** | PMT → DHU | 2.4GHz WiFi / LTE-M | 10km | 10Mbps |
| **L2** | DHU → RSS | 60GHz AirFiber / LTE | 50km | 1Gbps |
| **L3** | RSS → Cloud | 10GbE / AWS Direct | ∞ | 10Gbps |

**Critical Distinction:**

The FarmSense network uses **protocol blending** — combining 900MHz LoRa (penetration), 2.4GHz (bandwidth), 60GHz (backhaul), and LTE (fallback) to achieve coverage, capacity, and resilience simultaneously. No single protocol suffices; the orchestration of multiple protocols is the innovation.

**Key Differentiator:** The 900MHz CSS LoRa layer achieves **100% canopy penetration** in dense corn, where 2.4GHz suffers 60% loss. This ensures field data reaches the PMT even during peak growing season when crops are tallest.

---

## 2. Radio Protocol Stack

### 2.1 Layer 0: Sensor Network (900MHz CSS LoRa)

**Chirp Spread Spectrum (CSS) LoRa:**

| Parameter | Specification |
|-----------|---------------|
| **Frequency** | 915MHz (US ISM band) |
| **Modulation** | CSS LoRa (Chirp Spread Spectrum) |
| **Spreading Factor** | SF7 (fast) to SF12 (long range) |
| **Bandwidth** | 125kHz |
| **Coding Rate** | 4/5 |
| **Output Power** | +14dBm to +20dBm (25-100mW) |
| **Sensitivity** | -148dBm @ SF12 |
| **Range** | 5km+ line-of-sight, 1km dense canopy |
| **Data Rate** | 0.3kbps (SF12) to 5.5kbps (SF7) |

**Spontaneous Chirp Protocol:**

```python
class SpontaneousChirpProtocol:
    """
    ALOHA-based transmission with CSMA-CA collision avoidance
    """
    def __init__(self, device_id, spreading_factor=10):
        self.device_id = device_id
        self.sf = spreading_factor
        self.chirp_interval_base = 14400  # 4 hours in seconds
        
    def calculate_chirp_time(self, volatility_score):
        """
        Adaptive chirp interval based on field volatility
        
        Volatility Score (0-1):
        - 0.0-0.3: Stable, 4-hour chirps
        - 0.3-0.7: Active, 1-hour chirps
        - 0.7-1.0: Critical, 15-minute chirps
        """
        if volatility_score < 0.3:
            return self.chirp_interval_base  # 4 hours
        elif volatility_score < 0.7:
            return 3600  # 1 hour
        else:
            return 900  # 15 minutes
    
    def transmit(self, payload):
        """
        ALOHA transmission with listen-before-talk
        """
        # Listen for 50ms (one LoRa symbol @ SF10)
        if self.channel_clear(duration_ms=50):
            # Clear channel, transmit immediately
            self.lora_transmit(payload, self.sf)
            return True
        else:
            # Channel busy, exponential backoff
            backoff_ms = random.randint(100, 1000)
            time.sleep(backoff_ms / 1000)
            return self.transmit(payload)  # Retry
```

**Addressing Scheme:**

| Field | Size | Description |
|-------|------|-------------|
| Network ID | 2 bytes | Regional network (65,536 networks) |
| DHU ID | 1 byte | District hub (256 per network) |
| Field ID | 2 bytes | Field identifier (65,536 per DHU) |
| Device Type | 1 byte | VFA=0x01, LRZB=0x02, LRZN=0x03, PFA=0x04, PMT=0x05, CSA=0x06 |
| Device ID | 1 byte | Device number (256 per type) |
| **Total** | **7 bytes** | Unique device address |

Example: `0x01 0xA4 0x03 0x12 0x34 0x01 0x05` = Network 420, DHU 3, Field 4660, VFA #5

### 2.2 Layer 1: Field Aggregation (2.4GHz WiFi + LTE-M)

**WiFi 802.11ac Configuration:**

| Parameter | Specification |
|-----------|---------------|
| **Band** | 2.4GHz (channels 1, 6, 11) |
| **Mode** | AP (PMT) ↔ STA (DHU) or mesh |
| **Bandwidth** | 20MHz |
| **Data Rate** | Up to 150 Mbps |
| **Range** | 2km (outdoor, directional) |
| **Security** | WPA3-Enterprise, EAP-TLS |
| **Mesh** | 802.11s (PMT-to-PMT relay) |

**LTE Cat-M1 Configuration:**

| Parameter | Specification |
|-----------|---------------|
| **Bands** | B2 (1900MHz), B4 (1700MHz), B12 (700MHz), B13 (750MHz) |
| **Carrier** | T-Mobile / AT&T (dual-SIM) |
| **Data Rate** | 1Mbps uplink, 1Mbps downlink |
| **Latency** | 50-100ms to cloud |
| **Power** | 20dBm output |
| **Fallback** | Automatic on WiFi failure |

### 2.3 Layer 2: District Backhaul (60GHz AirFiber)

**Ubiquiti AirFiber 60:**

| Parameter | Specification |
|-----------|---------------|
| **Frequency** | 60GHz (unlicensed) |
| **Bandwidth** | 1Gbps full-duplex |
| **Range** | Up to 2km |
| **Latency** | <1ms |
| **Availability** | 99.99% (rain fade resistant) |
| **Antenna** | 38dBi dish |
| **Power** | 24VDC, 40W |

**Rain Fade Mitigation:**

| Rain Rate | Link Margin | Action |
|-----------|-------------|--------|
| < 10mm/hr | 10dB | Normal operation |
| 10-25mm/hr | 6dB | Modulation fallback |
| > 25mm/hr | 0dB | LTE backup activation |

### 2.4 Layer 3: Regional Uplink (10GbE)

**RSS Backhaul:**

| Parameter | Specification |
|-----------|---------------|
| **Primary** | Fiber optic (10GbE) |
| **Backup** | AWS Direct Connect |
| **Tertiary** | LTE (500Mbps bonded) |
| **Latency** | <5ms to AWS us-west-2 |
| **Redundancy** | Dual-path, automatic failover |

---

## 3. Network Topology

### 3.1 Field-Level Star (900MHz LoRa)

```
                    ┌─────────────────────┐
                    │      PMT (Master)    │
                    │   900MHz CSS LoRa    │
                    │   2.4GHz WiFi AP     │
                    └──────────┬───────────┘
                               │
        ┌────────────┬─────────┼─────────┬────────────┐
        │            │         │         │            │
    ┌───┴───┐   ┌───┴───┐ ┌───┴───┐ ┌───┴───┐   ┌───┴───┐
    │  VFA  │   │  LRZ  │ │  LRZ  │ │  LRZ  │   │  PFA  │
    │ × 2   │   │ B × 4 │ │ N × 12│ │ (16×) │   │ × 1   │
    │       │   │       │ │       │ │       │   │       │
    └───────┘   └───────┘ └───────┘ └───────┘   └───────┘
```

- **Star topology**: PMT as central hub
- **No meshing at sensor level**: Simplifies firmware, reduces power
- **Collision domain**: All sensors → single receiver (PMT)
- **Capacity**: 34 sensors max per PMT (hardware limit)

### 3.2 District Mesh (2.4GHz + AirFiber)

```
                        ┌───────────┐
                        │    RSS    │
                        │ (Oracle)  │
                        │ 60GHz AF  │
                        └─────┬─────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
              ┌─────┐   ┌─────┐   ┌─────┐
              │ DHU │   │ DHU │   │ DHU │
              │ #01 │   │ #02 │   │ #03 │
              └──┬──┘   └──┬──┘   └──┬──┘
                 │         │         │
         ┌───────┴───────┐ │ ┌───────┴───────┐
         │   WiFi Mesh   │ │ │   WiFi Mesh   │
         │               │ │ │               │
      ┌──┴──┐ ┌──┴──┐ ┌──┴─┴─┐ ┌──┴──┐ ┌──┴──┐
      │ PMT │ │ PMT │ │ PMT  │ │ PMT │ │ PMT │
      │ 101 │ │ 102 │ │ 103  │ │ 104 │ │ 105 │
      └──┬──┘ └──┬──┘ └──┬───┘ └──┬──┘ └──┬──┘
         │       │       │        │       │
      [Sensors] [Sensors] [Sensors] [Sensors] [Sensors]
```

- **Tree topology**: RSS → DHU → PMT → Sensors
- **DHU as relay**: Aggregates 100 PMTs
- **Redundant paths**: WiFi mesh enables PMT-to-PMT relay if DHU isolated
- **Self-healing**: Routes reconverge in <30 seconds

### 3.3 Regional Hub (10GbE)

```
┌────────────────────────────────────────────────────────────┐
│                        AWS Cloud                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │   EKS      │  │ RDS        │  │ S3 Glacier │            │
│  │ (Compute)  │  │ (Postgres) │  │ (Archive)  │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└────────────────────────────────────────────────────────────┘
                              │
                              │ 10GbE / AWS Direct Connect
                              │
                    ┌─────────┴─────────┐
                    │      RSS          │
                    │ (Regional Master) │
                    └─────────┬─────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
         ┌────┴────┐     ┌────┴────┐     ┌────┴────┐
         │  DHU    │     │  DHU    │     │  DHU    │
         │District1│     │District2│     │District3│
         │ (10×)   │     │ (10×)   │     │ (10×)   │
         └────┬────┘     └────┬────┘     └────┬────┘
              │               │               │
           [Fields]        [Fields]        [Fields]
```

---

## 4. Security Architecture

### 4.1 Encryption Layers

| Layer | Encryption | Key Management |
|-------|------------|----------------|
| **Sensor → PMT** | AES-128-CCM | Pre-shared per device |
| **PMT → DHU** | AES-256-GCM | ECDH session keys |
| **DHU → RSS** | ChaCha20-Poly1305 | TLS 1.3 |
| **RSS → Cloud** | AES-256-GCM | AWS KMS |
| **At Rest** | AES-256-XTS | Hardware security module |

### 4.2 Key Hierarchy

```
Root of Trust (HSM in RSS)
    │
    ├── Regional Key (RSS)
    │       ├── DHU Keys (10 per region)
    │       │       └── PMT Keys (100 per DHU)
    │       │               └── Device Keys (34 per PMT)
    │       │
    │       └── Cloud Key (AWS KMS)
    │
    └── Recovery Key (Offline, split custody)
```

### 4.3 Zero-Trust Principles

| Principle | Implementation |
|-----------|----------------|
| **Never trust, always verify** | Mutual authentication at every hop |
| **Least privilege** | Sensors can only report to PMT |
| **Assume breach** | Compromised PMT cannot access other fields |
| **Micro-segmentation** | Network isolation per field |

---

## 5. Failover & Resilience

### 5.1 Link Failure Scenarios

| Failure | Detection | Recovery | Data Loss |
|---------|-----------|----------|-----------|
| **Sensor → PMT** | Missed chirp (4hr) | None (dead sensor) | Until replacement |
| **PMT → DHU** | 5 missed beacons | LTE fallback | <1 hour |
| **DHU → RSS** | 3 missed uploads | LTE backup, local cache | <30 min |
| **RSS → Cloud** | 1 missed batch | LTE tertiary, tape queue | None (queued) |
| **Power outage** | Battery threshold | Generator auto-start | None (battery) |

### 5.2 Black Box Continuity

**DHU 30-Day Cache:**

| Trigger | Action | Result |
|---------|--------|--------|
| RSS unreachable | Store locally (Swissbit SSD) | 30 days retention |
| RSS restored | Upload backlog with timestamps | Complete recovery |
| Extended outage | Reduce sampling to 8-hour | Extend to 60 days |

**RSS 7-Year Vault:**

| Data Type | Local Storage | Cloud Mirror | Air Gap |
|-----------|---------------|--------------|---------|
| Compliance logs | 7 years | 7 years | LTO-9 tape |
| Raw telemetry | 30 days | 2 years | — |
| Kriging grids | 90 days | 7 years | Annual export |
| ML models | Current | All versions | — |

---

## 6. Protocol Specifications

### 6.1 LoRa Frame Format

```
┌─────────────────────────────────────────────────────────────┐
│ Preamble │ Header │ Payload │ MIC │ CRC                       │
│  8 bytes │ 4 bytes│ N bytes │4bytes│ 2 bytes                 │
└─────────────────────────────────────────────────────────────┘

Header Structure:
┌─────────┬─────────────┬──────────┬──────────────┐
│ DevAddr │ FCnt (16-bit)│ FCtrl    │ FPort       │
│ 4 bytes │ 2 bytes     │ 1 byte   │ 1 byte      │
└─────────┴─────────────┴──────────┴──────────────┘

Payload Structure (Device-Specific):
- VFA: 4-depth VWC + temp (16 bytes)
- LRZB: VWC + temp (8 bytes)
- LRZN: VWC only (4 bytes)
- PFA: Flow + pressure + CT (12 bytes)
```

### 6.2 WiFi Mesh Frame

```python
class MeshFrame:
    def __init__(self):
        self.header = {
            'version': 1,
            'type': 'DATA',  # DATA, BEACON, ROUTE
            'src_addr': 6,     # MAC address
            'dst_addr': 6,
            'hop_count': 1,
            'ttl': 32
        }
        self.payload = b''  # Encrypted data
        self.hmac = b''     # Authentication tag
        
    def route(self, routing_table):
        """802.11s mesh routing"""
        if self.header['dst_addr'] in routing_table:
            next_hop = routing_table[self.header['dst_addr']]
            return next_hop
        else:
            # Flood to all neighbors
            return 'BROADCAST'
```

---

## 7. Performance Benchmarks

### 7.1 Latency Budget

| Path | Target | Worst Case |
|------|--------|------------|
| **Sensor → PMT** | <100ms | <500ms (SF12) |
| **PMT → DHU** | <1s | <5s (LTE) |
| **DHU → RSS** | <5s | <30s (LTE backup) |
| **RSS → Cloud** | <1s | <10s (congestion) |
| **End-to-end** | <10s | <60s |

### 7.2 Throughput Requirements

| Entity | Daily Upload | Peak Burst |
|--------|--------------|------------|
| **Single Sensor** | 1 KB | 100 bytes @ 15min |
| **PMT (20 sensors)** | 50 KB | 5 KB @ 15min |
| **DHU (100 PMTs)** | 5 MB | 500 KB @ 15min |
| **RSS (10 DHUs)** | 50 MB | 5 MB @ 15min |
| **Region (1 RSS)** | 50 MB/day | 5 MB burst |

### 7.3 Reliability Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Packet delivery (L0)** | 99.9% | Per chirp acknowledgment |
| **Uptime (PMT)** | 99.5% | Annual availability |
| **Uptime (DHU)** | 99.9% | Annual availability |
| **Uptime (RSS)** | 99.99% | Annual availability |
| **Data completeness** | 99.95% | Valid records / expected |

---

## 8. Revision History

| Version | Date | Author | Changes | Approval |
|---------|------|--------|---------|----------|
| 1.0 | 2025-02-15 | J. Beebe | Initial network specification | Approved |
| 1.5 | 2025-09-01 | J. Beebe | Added 60GHz AirFiber, WiFi mesh | Approved |
| 2.0 | 2026-03-19 | J. Beebe | Expanded security, failover, performance | **PENDING** |

---

*Proprietary IP of bxthre3 inc. — Confidential*

---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
Document Code: DATA-SPEC
Full Name: FarmSense Data Architecture & Ingestion Specification
Version: 2.0
Category: Data Infrastructure & Governance
---

> [!IMPORTANT]
> **MODULAR DAP (Drift Aversion Protocol)**
> **Module: D-DAP (Documentation)**
> 
> 1. **Single Source of Truth**: This document is the authoritative reference for its subject matter.
> 2. **Synchronized Updates**: Any change to corresponding code or system behavior MUST be reflected here immediately.
> 3. **AI Agent Compliance**: Agents MUST verify the current implementation against this document before proposing changes.
> 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.
> 5. **ADDITIVE ONLY**: Details may only be added, never removed, summarized, or truncated.

---

# PART I: DATA ARCHITECTURE OVERVIEW

## 1.1 The Data Challenge

FarmSense generates heterogeneous, high-velocity telemetry from 8 device classes across 5 compute tiers. The data platform must:

- Ingest 50M+ sensor readings/day at Subdistrict scale
- Maintain sub-second query latency for real-time irrigation decisions
- Preserve 7-year immutable audit trails for Water Court admissibility
- Enable 1-meter spatial resolution via Kriging interpolation
- Support federated learning without raw data export
- Ensure zero data loss during network partitions

## 1.2 Data Classification Matrix

| Data Class | Source | Velocity | Volume | Retention | Criticality |
|------------|--------|----------|--------|-----------|-------------|
| **Hot Telemetry** | LRZN/LRZB/VFA/PFA/PMT | 4hr-15min intervals | 45M/day | 90 days | Real-time irrigation |
| **Compliance Ledger** | All devices + human entry | Event-driven | 500K/day | 7 years | Legal admissibility |
| **Spatial Grids** | Kriging engines (PMT/DHU/RSS) | 1hr-15min | 2M tiles/day | 2 years | 1m resolution |
| **Audit Proofs** | PBFT consensus | Per commit | 100K/day | 10 years | Tamper evidence |
| **ML Training** | Aggregated features | Daily batches | 10GB/day | Indefinite | Model improvement |
| **System Health** | Infrastructure metrics | 60s intervals | 50M/day | 30 days | Ops monitoring |

## 1.3 Tri-Layer Data Topology

**Level 0 — Edge Sensors (Field):**
- Local storage: 128KB-4MB (circular buffers)
- Protocol: 900MHz CSS LoRa → PMT
- Encryption: AES-128 at edge
- Resilience: Store-and-forward during outages

**Level 1.5 — PMT Hub (Edge Aggregation):**
- Buffer: 187-byte state packets, 72-hour retention
- Processing: Edge-EBK 50m grid calculation
- Protocol: 2.4GHz/LTE-M → DHU
- Downlink: Worksheet delivery to pivot controller

**Level 2 — DHU (District Edge):**
- Cache: 128GB PSLC SSD (30-day Black Box)
- Processing: 20m/10m Kriging, PBFT consensus
- Protocol: 60GHz/LTE/Starlink → RSS

**Level 3 — RSS (Regional Master):**
- Storage: 50TB NVMe (hot), 200TB HDD (warm)
- Processing: 1m Master Grid, Regression Kriging
- Vault: FHE-encrypted compliance ledger

**Level 4 — Cloud (Zo Infrastructure):**
- Storage: TimescaleDB (hot), S3/Glacier (cold)
- Processing: Global analytics, ML training
- Resilience: Multi-AZ, automated failover

---

# PART II: DATABASE SCHEMA SPECIFICATION

## 2.1 TimescaleDB Time-Series Schema

### 2.1.1 Core Telemetry Table

```sql
-- Primary sensor readings hypertable
CREATE TABLE sensor_readings (
    time TIMESTAMPTZ NOT NULL,
    device_id UUID NOT NULL,
    field_id UUID NOT NULL,
    sensor_type VARCHAR(50) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    quality_score FLOAT CHECK (quality_score >= 0 AND quality_score <= 1),
    location GEOGRAPHY(POINT, 4326),
    metadata JSONB,
    PRIMARY KEY (time, device_id, sensor_type)
);

-- Enable time-series partitioning
SELECT create_hypertable('sensor_readings', 'time', 
    chunk_time_interval => INTERVAL '7 days',
    if_not_exists => TRUE
);

-- Compression policy (30-day delay, 90% compression target)
SELECT add_compression_policy('sensor_readings', INTERVAL '30 days');

-- Retention policy (cold storage after 2 years)
SELECT add_retention_policy('sensor_readings', INTERVAL '2 years');
```

### 2.1.2 Telemetry Indexes

```sql
-- Device time-series queries (most common)
CREATE INDEX idx_sensor_device_time 
    ON sensor_readings(device_id, time DESC);

-- Field aggregation queries
CREATE INDEX idx_sensor_field_time 
    ON sensor_readings(field_id, time DESC);

-- Spatial queries for Kriging
CREATE INDEX idx_sensor_location 
    ON sensor_readings USING GIST(location);

-- Sensor type filtering
CREATE INDEX idx_sensor_type_time 
    ON sensor_readings(sensor_type, time DESC);

-- Quality score filtering (exclude low-confidence)
CREATE INDEX idx_sensor_quality 
    ON sensor_readings(quality_score) WHERE quality_score < 0.8;
```

### 2.1.3 Device State Table

```sql
-- Current device state (latest reading per sensor)
CREATE TABLE device_state (
    device_id UUID PRIMARY KEY,
    field_id UUID NOT NULL REFERENCES fields(id),
    device_type VARCHAR(20) NOT NULL,
    last_seen TIMESTAMPTZ NOT NULL,
    battery_voltage FLOAT,
    rssi_dbm INTEGER,
    firmware_version VARCHAR(20),
    sensor_states JSONB, -- {"moisture_10cm": {"value": 0.234, "time": "..."}}
    alerts JSONB, -- Active alert conditions
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trigger to auto-update device_state from sensor_readings
CREATE OR REPLACE FUNCTION update_device_state()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO device_state (device_id, field_id, last_seen, sensor_states, updated_at)
    SELECT 
        NEW.device_id,
        NEW.field_id,
        NEW.time,
        jsonb_build_object(
            NEW.sensor_type, jsonb_build_object(
                'value', NEW.value,
                'time', NEW.time,
                'quality', NEW.quality_score
            )
        ),
        NOW()
    ON CONFLICT (device_id) DO UPDATE SET
        last_seen = NEW.time,
        sensor_states = device_state.sensor_states || EXCLUDED.sensor_states,
        updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_device_state
    AFTER INSERT ON sensor_readings
    FOR EACH ROW EXECUTE FUNCTION update_device_state();
```

## 2.2 PostgreSQL Compliance Schema

### 2.2.1 Compliance Ledger (Tamper-Evident)

```sql
-- Hash-chained compliance log for Water Court admissibility
CREATE TABLE compliance_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    field_id UUID NOT NULL REFERENCES fields(id) ON DELETE CASCADE,
    log_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    event_type VARCHAR(50) NOT NULL,
    details JSONB NOT NULL,
    hash VARCHAR(64) NOT NULL,
    previous_hash VARCHAR(64),
    pbft_signature BYTEA,
    created_by UUID REFERENCES users(id),
    
    CONSTRAINT valid_event_type CHECK (event_type IN (
        'IRRIGATION_START', 
        'IRRIGATION_STOP', 
        'VIOLATION_DETECTED',
        'VIOLATION_RESOLVED',
        'PBFT_COMMIT',
        'CALIBRATION',
        'MAINTENANCE',
        'AUDIT_EXPORT',
        'THRESHOLD_BREACH',
        'PUMP_SHUTDOWN'
    ))
);

-- Hash chaining index for verification
CREATE INDEX idx_compliance_chain 
    ON compliance_logs(field_id, log_time);

-- Event type filtering
CREATE INDEX idx_compliance_events 
    ON compliance_logs(event_type, log_time DESC);

-- Immutable audit retention (no automatic deletion)
ALTER TABLE compliance_logs SET (timescaledb.compress = false);
```

### 2.2.2 Ledger Integrity Functions

```sql
-- Verify hash chain integrity for a field
CREATE OR REPLACE FUNCTION verify_compliance_chain(field_uuid UUID)
RETURNS TABLE (
    log_id UUID,
    log_time TIMESTAMPTZ,
    hash_valid BOOLEAN,
    chain_valid BOOLEAN,
    error_message TEXT
) AS $$
DECLARE
    prev_hash VARCHAR(64) := NULL;
    calculated_hash VARCHAR(64);
    record RECORD;
BEGIN
    FOR record IN 
        SELECT * FROM compliance_logs 
        WHERE field_id = field_uuid 
        ORDER BY log_time
    LOOP
        -- Calculate expected hash
        calculated_hash := encode(
            digest(
                record.field_id::text || 
                record.log_time::text || 
                record.event_type || 
                record.details::text ||
                COALESCE(prev_hash, ''),
                'sha256'
            ),
            'hex'
        );
        
        RETURN QUERY SELECT 
            record.id,
            record.log_time,
            (record.hash = calculated_hash),
            (record.previous_hash IS NULL OR record.previous_hash = prev_hash),
            CASE 
                WHEN record.hash != calculated_hash THEN 'Hash mismatch'
                WHEN record.previous_hash != prev_hash THEN 'Chain break'
                ELSE NULL
            END;
        
        prev_hash := record.hash;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## 2.3 PostGIS Spatial Schema

### 2.3.1 Field Boundaries

```sql
-- Field polygons with geospatial indexing
CREATE TABLE fields (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    owner_id UUID NOT NULL REFERENCES users(id),
    organization_id UUID REFERENCES organizations(id),
    
    -- Geometry
    geometry GEOGRAPHY(POLYGON, 4326) NOT NULL,
    center GEOGRAPHY(POINT, 4326),
    area_ha FLOAT GENERATED ALWAYS AS (
        ST_Area(geometry::geography) / 10000
    ) STORED,
    
    -- Soil properties
    soil_type VARCHAR(50),
    soil_texture VARCHAR(20),
    dominant_soil_series VARCHAR(100),
    avg_slope_percent FLOAT,
    
    -- Irrigation configuration
    pivot_count INTEGER DEFAULT 0,
    pivot_radius_m FLOAT,
    water_source VARCHAR(50), -- 'groundwater', 'surface', 'mixed'
    
    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deactivated_at TIMESTAMPTZ,
    
    -- Spatial indexes
    CONSTRAINT valid_geometry CHECK (ST_IsValid(geometry::geometry))
);

-- Spatial indexes
CREATE INDEX idx_fields_geometry ON fields USING GIST(geometry);
CREATE INDEX idx_fields_center ON fields USING GIST(center);
CREATE INDEX idx_fields_owner ON fields(owner_id);
CREATE INDEX idx_fields_org ON fields(organization_id);
```

### 2.3.2 Kriging Grid Tiles

```sql
-- Raster tiles for moisture visualization
CREATE TABLE kriging_grids (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    field_id UUID NOT NULL REFERENCES fields(id),
    
    -- Grid properties
    resolution_m INTEGER NOT NULL, -- 1, 10, 20, 50
    depth_cm INTEGER, -- NULL for surface, or 10, 30, 60
    
    -- Timestamp
    computed_at TIMESTAMPTZ NOT NULL,
    computation_time_ms INTEGER, -- Performance tracking
    
    -- Kriging parameters used
    variogram_model VARCHAR(20),
    nugget FLOAT,
    sill FLOAT,
    range_m FLOAT,
    
    -- Grid data as JSONB (compressed 1m raster)
    -- Format: {"width": 800, "height": 600, "values": [0.234, 0.235, ...], "nodata": -9999}
    grid_data JSONB NOT NULL,
    
    -- Quality metrics
    mape FLOAT, -- Mean Absolute Percentage Error
    rmse FLOAT, -- Root Mean Square Error
    sensor_count INTEGER,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for grid queries
CREATE INDEX idx_kriging_field_resolution 
    ON kriging_grids(field_id, resolution_m, depth_cm, computed_at DESC);

-- Automatic cleanup of old low-res grids (keep latest 30 days)
SELECT add_retention_policy('kriging_grids', INTERVAL '30 days');
```

---

# PART III: DATA INGESTION PIPELINE

## 3.1 Ingestion Architecture

### 3.1.1 Pipeline Flow

```
┌─────────────┐    LoRa 900MHz    ┌─────────────┐    2.4GHz/LTE    ┌─────────────┐
│  LRZN/LRZB  │ ─────────────────→ │     PMT     │ ────────────────→│     DHU     │
│  VFA/PFA    │   CSS, AES-128   │   (Edge)    │   MQTT+TLS       │  (District) │
└─────────────┘                    └─────────────┘                  └─────────────┘
                                                                           │
                                                                           │ 60GHz/LTE
                                                                           ↓
┌─────────────┐                  ┌─────────────┐    TLS 1.3         ┌─────────────┐
│   Cloud     │ ←────────────────│     RSS     │ ←──────────────────│     DHU     │
│  (Zo/AWS)   │   Kafka/Fargate  │  (Regional) │   Starlink/Optic  │  (District) │
└─────────────┘                  └─────────────┘                   └─────────────┘
```

### 3.1.2 Protocol Stack by Tier

| Tier | Uplink Protocol | Payload Format | Encryption | Reliability |
|------|-----------------|----------------|------------|-------------|
| Sensors → PMT | 900MHz LoRa CSS | Protobuf (50 bytes) | AES-128-GCM | Confirmed uplink |
| PMT → DHU | 2.4GHz 802.11n | MQTT over TLS | TLS 1.3 | QoS 1 (at-least-once) |
| DHU → RSS | 60GHz/5GHz/LTE | gRPC over TLS | mTLS + JWT | QoS 2 (exactly-once) |
| RSS → Cloud | 10Gbps fiber | Kafka Protocol | TLS 1.3 + cert pinning | Idempotent producers |

## 3.2 Sensor Ingestion API

### 3.2.1 Telemetry Ingest Endpoint

```yaml
# OpenAPI 3.0 specification
openapi: 3.0.0
info:
  title: FarmSense Telemetry Ingest API
  version: 2.0.0

paths:
  /v2/ingest/telemetry:
    post:
      summary: Ingest sensor telemetry batch
      description: |
        Accepts batched sensor readings from field devices.
        Supports up to 100 readings per request.
        Returns 202 Accepted for async processing.
      
      security:
        - mTLS: []
        - BearerAuth: []
      
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TelemetryBatch'
            example:
              device_id: "550e8400-e29b-41d4-a716-446655440000"
              field_id: "660e8400-e29b-41d4-a716-446655440001"
              batch_time: "2026-03-19T14:30:00Z"
              readings:
                - sensor_type: "vwc_30cm"
                  value: 0.234
                  timestamp: "2026-03-19T14:30:00Z"
                  quality_score: 0.98
                  metadata:
                    battery_v: 3.65
                    rssi_dbm: -85
                    temperature_c: 22.5
      
      responses:
        '202':
          description: Accepted for processing
          content:
            application/json:
              schema:
                type: object
                properties:
                  batch_id:
                    type: string
                    format: uuid
                  ingested:
                    type: integer
                  errors:
                    type: array
                    items:
                      $ref: '#/components/schemas/IngestError'
        
        '400':
          description: Validation error
        '401':
          description: Authentication required
        '429':
          description: Rate limit exceeded

components:
  schemas:
    TelemetryBatch:
      type: object
      required:
        - device_id
        - field_id
        - readings
      properties:
        device_id:
          type: string
          format: uuid
        field_id:
          type: string
          format: uuid
        batch_time:
          type: string
          format: date-time
        readings:
          type: array
          maxItems: 100
          items:
            $ref: '#/components/schemas/SensorReading'
    
    SensorReading:
      type: object
      required:
        - sensor_type
        - value
        - timestamp
      properties:
        sensor_type:
          type: string
          enum: [vwc_10cm, vwc_30cm, vwc_60cm, temperature, ec, battery, rssi]
        value:
          type: number
        timestamp:
          type: string
          format: date-time
        quality_score:
          type: number
          minimum: 0
          maximum: 1
        metadata:
          type: object
          additionalProperties: true
    
    IngestError:
      type: object
      properties:
        reading_index:
          type: integer
        error_code:
          type: string
        message:
          type: string
  
  securitySchemes:
    mTLS:
      type: mutualTLS
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### 3.2.2 Field State Update (PMT Downlink)

```protobuf
// Protocol Buffer for PMT-to-Cloud state updates
syntax = "proto3";
package farmsense.ingest.v2;

message FieldStatePacket {
  // Identifiers
  string pmt_id = 1;
  string field_id = 2;
  
  // Timestamp
  google.protobuf.Timestamp timestamp = 3;
  
  // Pivot kinematics
  PivotState pivot = 4;
  
  // Aggregated sensor data
  repeated SensorSnapshot sensors = 5;
  
  // Kriging output (50m grid)
  KrigingGrid moisture_grid = 6;
  
  // System status
  SystemHealth health = 7;
  
  // Cryptographic signature
  bytes signature = 8;
}

message PivotState {
  // RTK-corrected position
  double latitude = 1;
  double longitude = 2;
  float accuracy_cm = 3;
  
  // Pivot kinematics
  float angle_degrees = 4;
  float speed_percent = 5;
  bool is_moving = 6;
  
  // IMU stall detection
  float accel_x = 7;
  float accel_y = 8;
  float accel_z = 9;
  
  // Status
  uint32 last_gnss_fix_ms = 10;
}

message SensorSnapshot {
  string device_id = 1;
  string device_type = 2;  // VFA, LRZN, LRZB, PFA
  
  // Last reading
  google.protobuf.Timestamp last_seen = 3;
  
  // Aggregated values
  float battery_voltage = 4;
  int32 rssi_dbm = 5;
  
  // Sensor-specific values
  map<string, float> readings = 6;  // {"vwc_30cm": 0.234}
  
  // Quality flags
  bool is_healthy = 7;
  string alert_flags = 8;
}

message KrigingGrid {
  uint32 width = 1;
  uint32 height = 2;
  float resolution_m = 3;
  
  // ZLib-compressed float array
  bytes compressed_values = 4;
  
  // Grid bounds
  BoundingBox bounds = 5;
  
  // Quality
  float mape = 6;
  uint32 sensor_count = 7;
}

message SystemHealth {
  float battery_percent = 1;
  float cpu_temp_c = 2;
  uint32 free_memory_mb = 3;
  
  // Network
  int32 uplink_rssi = 4;
  string uplink_type = 5;  // LTE, WIFI, SATCOM
  
  // Queue depths
  uint32 pending_uplink_bytes = 6;
  uint32 dropped_packets_24h = 7;
  
  // Firmware
  string firmware_version = 8;
  uint32 uptime_seconds = 9;
}
```

## 3.3 Data Validation Rules

### 3.3.1 Sensor Reading Validation

| Sensor Type | Value Range | Rate Limit | Quality Score Logic |
|-------------|-------------|------------|---------------------|
| vwc_* | 0.0 - 1.0 | 4hr-15min | Decay from 1.0 based on age |
| temperature | -40°C - +60°C | 4hr | 0.8 if calibration drift > 2°C |
| ec | 0 - 5 dS/m | 4hr | 0.6 if sensor degradation detected |
| battery | 2.8V - 4.2V | 1hr | 0.0 if < 3.0V (critical) |
| rssi | -148dBm - 0dBm | Per packet | 1.0 if > -100dBm, 0.5 if < -120dBm |

### 3.3.2 Anomaly Detection Pipeline

```python
# Pseudocode for data quality pipeline
class DataQualityEngine:
    def validate_reading(self, reading: SensorReading) -> ValidatedReading:
        # 1. Range validation
        if not self._in_range(reading.sensor_type, reading.value):
            return self._flag_anomaly(reading, "RANGE_VIOLATION")
        
        # 2. Temporal consistency
        history = self._get_recent_history(reading.device_id, hours=24)
        if self._is_temporal_outlier(reading, history):
            return self._flag_anomaly(reading, "TEMPORAL_OUTLIER")
        
        # 3. Cross-sensor validation
        if reading.sensor_type.startswith("vwc_"):
            neighbors = self._get_spatial_neighbors(reading.location, radius=50)
            if self._deviates_from_neighbors(reading, neighbors, threshold=0.1):
                reading.quality_score *= 0.8
                reading.flags.append("SPATIAL_DEVIATION")
        
        # 4. Physical plausibility
        if not self._is_physically_plausible(reading, history):
            return self._flag_anomaly(reading, "PHYSICAL_IMPLAUSIBILITY")
        
        return reading
    
    def compute_quality_score(self, reading: SensorReading) -> float:
        base_score = 1.0
        
        # Age decay
        age_hours = (now() - reading.timestamp).hours
        if age_hours > 4:
            base_score *= 0.9 ** (age_hours - 4)
        
        # Battery impact
        if reading.metadata.get("battery_v", 3.7) < 3.2:
            base_score *= 0.7
        
        # RSSI impact
        rssi = reading.metadata.get("rssi_dbm", -100)
        if rssi < -120:
            base_score *= 0.8
        
        return max(0.0, min(1.0, base_score))
```

---

# PART IV: DATA RETENTION & ARCHIVAL

## 4.1 Tiered Storage Strategy

| Tier | Data Age | Storage | Compression | Access Pattern |
|------|----------|---------|-------------|----------------|
| Hot | 0-90 days | EBS io2 SSD | None | Real-time queries |
| Warm | 90 days - 2 years | EBS gp3 | TimescaleDB native | Analytics queries |
| Cold | 2-7 years | S3 Standard-IA | Parquet + Zstd | Compliance exports |
| Vault | 7+ years | Glacier Deep Archive | Parquet + Zstd | Legal hold only |

## 4.2 Automated Archival Pipeline

```python
# Daily archival job (AWS Lambda)
def archive_partition(partition_date: date):
    # 1. Query hot data for partition
    readings = query_timescaledb(
        f"""
        SELECT * FROM sensor_readings
        WHERE time >= '{partition_date}' 
          AND time < '{partition_date + 1 day}'
        """
    )
    
    # 2. Convert to columnar format
    df = pandas.DataFrame(readings)
    table = pyarrow.Table.from_pandas(df)
    
    # 3. Compress with Zstd
    pq.write_table(
        table, 
        f"s3://farmsense-archive/{partition_date}.parquet",
        compression="zstd",
        row_group_size=100000
    )
    
    # 4. Update archival registry
    register_archived_partition(partition_date, s3_path)
    
    # 5. Mark for deletion from hot (soft delete)
    mark_partition_archived(partition_date)
```

## 4.3 Water Court Compliance Export

```sql
-- Generate Digital Water Ledger for legal discovery
CREATE OR REPLACE FUNCTION export_compliance_ledger(
    field_uuid UUID,
    start_date DATE,
    end_date DATE
) RETURNS TABLE (
    export_id UUID,
    manifest JSONB,
    zip_path TEXT
) AS $$
DECLARE
    export_uuid UUID := gen_random_uuid();
    s3_path TEXT;
BEGIN
    -- 1. Create ZIP bundle with:
    --    - manifest.json (metadata)
    --    - ledger.csv (all compliance events)
    --    - proofs/*.sig (PBFT signatures)
    --    - validation_report.pdf
    --    - hash_chain_verification.json
    
    s3_path := perform_export(field_uuid, start_date, end_date, export_uuid);
    
    -- 2. Log export for audit trail
    INSERT INTO compliance_exports (id, field_id, start_date, end_date, s3_path)
    VALUES (export_uuid, field_uuid, start_date, end_date, s3_path);
    
    RETURN QUERY SELECT export_uuid, 
        jsonb_build_object(
            'field_id', field_uuid,
            'date_range', start_date || ' to ' || end_date,
            'record_count', (SELECT count(*) FROM compliance_logs 
                           WHERE field_id = field_uuid 
                           AND log_time BETWEEN start_date AND end_date),
            'hash_verification', verify_compliance_chain(field_uuid)
        ),
        s3_path;
END;
$$ LANGUAGE plpgsql;
```

---

# PART V: DATA GOVERNANCE & SECURITY

## 5.1 Access Control Matrix

| Role | Hot Telemetry | Compliance Ledger | Kriging Grids | Device Config |
|------|---------------|-------------------|---------------|---------------|
| Farmer (Owner) | Read own | Read own | Read own | Read/Write own |
| Farm Manager | Read assigned | Read assigned | Read assigned | Read assigned |
| Auditor | None | Read (time-bounded) | None | None |
| Data Scientist | Anonymized aggregates | None | Anonymized | None |
| System | Full | Full | Full | Full |

## 5.2 Encryption Standards

| Layer | Method | Key Management |
|-------|--------|----------------|
| At-rest (Hot) | AES-256-XTS | AWS KMS CMK |
| At-rest (Cold) | AES-256-GCM | S3 SSE-KMS |
| In-transit (field) | AES-128-GCM | Device embedded key |
| In-transit (backhaul) | TLS 1.3 + mTLS | Let's Encrypt + internal CA |
| Compliance ledger | FHE (BFV scheme) | HSM in RSS airgap |

## 5.3 Privacy-Preserving Analytics

### 5.3.1 Differential Privacy

```python
# Federated learning with DP
class DPQueryEngine:
    def __init__(self, epsilon: float = 1.0, delta: float = 1e-6):
        self.epsilon = epsilon
        self.delta = delta
        self.noise_multiplier = compute_noise_multiplier(epsilon, delta)
    
    def query_average_vwc(self, field_ids: List[UUID]) -> float:
        # Get true average
        true_avg = db.query(
            "SELECT AVG(value) FROM sensor_readings "
            "WHERE field_id = ANY(:field_ids)",
            field_ids=field_ids
        )
        
        # Add Gaussian noise for DP
        sensitivity = 1.0 / len(field_ids)  # Global sensitivity
        noise = np.random.normal(0, self.noise_multiplier * sensitivity)
        
        return true_avg + noise
```

### 5.3.2 Contextual Anonymization

- **Operational Analytics**: Field-level aggregation, no PII
- **Compliance Ledger**: Immutable with field IDs (legal requirement)
- **ML Training**: Differentially private gradients only
- **Research Partnerships**: Synthetic data generation from fitted models

---

# PART VI: DATA LINEAGE & OBSERVABILITY

## 6.1 Data Lineage Tracking

Every derived dataset maintains provenance:

```json
{
  "lineage": {
    "dataset_id": "kriging-grid-field-123-20260319",
    "derived_from": [
      {
        "source": "sensor_readings",
        "filter": "field_id = '123' AND time >= '2026-03-19'",
        "row_count": 15432
      }
    ],
    "transformations": [
      {
        "name": "kriging_ordinary",
        "parameters": {
          "variogram": "spherical",
          "nugget": 0.0012,
          "sill": 0.0085,
          "range": 245
        },
        "code_version": "kriging-engine:v2.3.1"
      }
    ],
    "computed_at": "2026-03-19T14:30:00Z",
    "computed_by": "dhu-district-5",
    "mape": 0.043
  }
}
```

## 6.2 Observability Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Ingestion latency (p99) | < 5 seconds | > 30 seconds |
| Query latency (hot data) | < 100ms | > 500ms |
| Data freshness (Kriging) | < 15 minutes | > 1 hour |
| Archive lag | < 24 hours | > 72 hours |
| Missing sensor rate | < 2% | > 10% |
| Hash chain integrity | 100% | Any failure |

---

# PART VII: DISASTER RECOVERY

## 7.1 Backup Strategy

| Data Class | Frequency | Retention | Recovery RTO |
|------------|-----------|-----------|--------------|
| Hot TimescaleDB | Continuous (WAL) | 7 days | < 1 hour |
| Compliance Ledger | Real-time replication | 7 years | < 4 hours |
| Spatial Grids | Daily snapshots | 30 days | < 2 hours |
| Device Config | On-change | Indefinite | < 30 minutes |

## 7.2 Multi-Region Failover

- **Primary**: AWS us-west-2 (Oregon)
- **Secondary**: AWS us-east-1 (Virginia)
- **Tertiary**: On-prem RSS (airgap capable)

**Failover Triggers**:
- Primary region unavailable > 5 minutes
- Database replication lag > 10 minutes
- Manual executive decision

---

# PART VIII: DATA API REFERENCE

## 8.1 Query Endpoints

```
GET /v2/fields/{id}/moisture
  ?depth=30cm
  &resolution=1m
  &timestamp=2026-03-19T14:30:00Z

POST /v2/query/aggregate
  {
    "field_ids": ["uuid1", "uuid2"],
    "metric": "avg_vwc",
    "depth": 30,
    "time_range": {"start": "...", "end": "..."},
    "group_by": "day"
  }

GET /v2/compliance/export
  ?field_id={uuid}
  &start_date=2026-01-01
  &end_date=2026-03-31
  &format=dwl

WS /v2/stream/field/{id}
  → Real-time moisture updates
  → Irrigation events
  → Alert notifications
```

## 8.2 Rate Limits

| Endpoint | Tier | Burst | Per-Minute |
|----------|------|-------|------------|
| /v2/ingest/* | Device | 100 | 10,000 |
| /v2/fields/* | User | 100 | 1,000 |
| /v2/compliance/* | Auditor | 10 | 100 |
| /v2/stream/* | User | 5 connections | — |

---

# APPENDIX A: DATA DICTIONARY

## A.1 Sensor Type Codes

| Code | Description | Unit | Precision |
|------|-------------|------|-----------|
| vwc_10cm | Volumetric water content at 10cm | m³/m³ | 0.001 |
| vwc_30cm | Volumetric water content at 30cm | m³/m³ | 0.001 |
| vwc_60cm | Volumetric water content at 60cm | m³/m³ | 0.001 |
| temp_10cm | Soil temperature at 10cm | °C | 0.1 |
| ec_10cm | Electrical conductivity at 10cm | dS/m | 0.01 |
| battery | Device battery voltage | V | 0.01 |
| rssi | Signal strength | dBm | 1 |
| flow_rate | Well flow rate | GPM | 0.1 |
| pressure | Wellhead pressure | PSI | 0.1 |
| pivot_angle | Pivot rotation angle | ° | 0.1 |
| pivot_speed | Pivot speed | % | 1 |

## A.2 Device Type Codes

| Code | Full Name | Tier | Uplink Interval |
|------|-----------|------|-----------------|
| LRZN | Lateral Root Zone Node | 0 | 4hr (15min ripple) |
| LRZB | Lateral Root Zone Beacon | 0 | 4hr (15min ripple) |
| VFA | Vertical Field Anchor | 0 | 4hr (15min ripple) |
| PFA | Pressure & Flow Analyzer | 0 | 1hr (5min active) |
| CSA | Corner Swing Arm | 0 | 4hr (15min ripple) |
| PMT | Pivot Motion Tracker | 1.5 | 60s (5s active) |
| DHU | District Hub Unit | 2 | 15min |
| RSS | Regional Superstation | 3 | 5min |

---

*Document Version: 2.0*
*Last Comprehensive Review: 2026-03-19*
*Next Scheduled Review: 2026-06-19*
*Owner: Data Engineering Team*
*DAP Compliance: VERIFIED*

**Proprietary & Confidential — bxthre3 inc.**

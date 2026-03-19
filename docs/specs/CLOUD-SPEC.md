---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
System Code: CLD
Full Name: FarmSense Cloud Infrastructure
Version: 2.0
Category: Cloud Architecture & Services
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

# CLOUD V2.0: FarmSense Cloud Infrastructure

## 1. Executive Summary

### 1.1 Role and Function

The FarmSense Cloud Infrastructure is the **global intelligence layer** — the AWS-hosted compute environment that receives regional data, trains ML models, serves the web application, maintains long-term archives, and provides API access to third-party integrators. While field and edge devices handle real-time operations, the cloud provides historical analysis, model improvement, farmer dashboards, and regulatory reporting.

**Primary Functions:**

1. **Data Ingestion**: Receive telemetry from regional superstations
2. **Model Training**: LSTM forecasting, Kriging optimization
3. **Web Application**: React-based farmer dashboard
4. **Compliance Reporting**: Digital Water Ledger exports
5. **Third-Party APIs**: Integration with banking, insurance, markets
6. **Long-Term Archive**: 7-year retention for Water Court
7. **Disaster Recovery**: Multi-region failover

**Cloud Hierarchy:**

| Layer | Service | Purpose |
|-------|---------|---------|
| **Compute** | AWS EKS (Kubernetes) | Container orchestration |
| **Database** | RDS PostgreSQL + TimescaleDB | Time-series telemetry |
| **Cache** | ElastiCache Redis | Session, real-time data |
| **Storage** | S3 + Glacier | Raw data, archives |
| **ML** | SageMaker | Model training, inference |
| **Network** | CloudFront, Route53 | CDN, DNS |
| **Security** | IAM, KMS, WAF | Auth, encryption, firewall |

**Critical Distinction:**

| Entity | Local Data | Cloud Data |
|--------|------------|------------|
| **Sensor** | 1 chirp | None (ephemeral) |
| **PMT** | 24 hours | Forward-only |
| **DHU** | 30 days | Aggregate batches |
| **RSS** | 7 years | Compliance archives |
| **Cloud** | N/A | Permanent, analytics |

**Key Differentiator:** The cloud is **non-critical for operations** — a field can operate for 30 days without cloud connectivity (DHU Black Box), and for 7 years without losing compliance data (RSS vault). The cloud adds value through analytics, ML, and convenience, but the deterministic edge is sovereign.

---

## 2. AWS Architecture

### 2.1 Regional Deployment

**Primary Region: AWS us-west-2 (Oregon)**

| Service | Configuration | Purpose |
|---------|---------------|---------|
| **EKS** | 3× m6i.2xlarge nodes | Kubernetes workloads |
| **RDS** | db.r6g.2xlarge, Multi-AZ | PostgreSQL primary |
| **ElastiCache** | cache.r6g.large | Redis cluster |
| **S3** | Standard + Intelligent-Tiering | Object storage |
| **SageMaker** | ml.m5.2xlarge | Training jobs |
| **CloudFront** | Edge locations | Static asset delivery |
| **Route53** | Health checks | DNS failover |

**Disaster Recovery: AWS us-east-1 (Virginia)**

| Service | Configuration | RPO | RTO |
|---------|---------------|-----|-----|
| **RDS** | Cross-region read replica | 5 min | 15 min |
| **S3** | Cross-region replication | 0 | Immediate |
| **EKS** | Standby cluster | — | 30 min |

### 2.2 Kubernetes (EKS) Architecture

```yaml
# Namespace structure
namespaces:
  - production
  - staging
  - ml-training
  - compliance

# Core deployments
services:
  - name: api-gateway
    replicas: 3
    resources:
      requests: {cpu: 500m, memory: 512Mi}
      limits: {cpu: 2000m, memory: 2Gi}
  
  - name: telemetry-ingest
    replicas: 5
    hpa: {min: 5, max: 50, targetCPU: 70%}
    resources:
      requests: {cpu: 1000m, memory: 2Gi}
  
  - name: kriging-worker
    replicas: 3
    resources:
      requests: {cpu: 2000m, memory: 8Gi}  # GPU later
  
  - name: web-app
    replicas: 3
    resources:
      requests: {cpu: 250m, memory: 256Mi}
  
  - name: compliance-exporter
    replicas: 2
    resources:
      requests: {cpu: 500m, memory: 1Gi}
```

### 2.3 Database Schema (RDS PostgreSQL + TimescaleDB)

**TimescaleDB Hypertables:**

```sql
-- Sensor telemetry (partitioned by time)
CREATE TABLE sensor_telemetry (
    time TIMESTAMPTZ NOT NULL,
    device_id UUID NOT NULL,
    field_id UUID NOT NULL,
    device_type VARCHAR(10) NOT NULL,  -- VFA, LRZB, LRZN, PFA, PMT
    metric_name VARCHAR(50) NOT NULL,  -- vwc_10cm, temp, flow_rate
    value DOUBLE PRECISION NOT NULL,
    quality_score FLOAT CHECK (quality_score >= 0 AND quality_score <= 1),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    metadata JSONB,
    PRIMARY KEY (time, device_id, metric_name)
);

-- Create hypertable with 1-day chunks
SELECT create_hypertable('sensor_telemetry', 'time', 
                       chunk_time_interval => INTERVAL '1 day');

-- Compression after 7 days
ALTER TABLE sensor_telemetry SET (
    timescaledb.compress = true,
    timescaledb.compress_segmentby = 'device_id',
    timescaledb.compress_orderby = 'time DESC'
);

-- Retention: 2 years compressed, then Glacier
SELECT add_retention_policy('sensor_telemetry', INTERVAL '2 years');

-- Kriging grid results
CREATE TABLE kriging_grids (
    time TIMESTAMPTZ NOT NULL,
    field_id UUID NOT NULL,
    resolution VARCHAR(10) NOT NULL,  -- 1m, 10m, 20m, 50m
    grid_data BYTEA NOT NULL,  -- Compressed raster
    confidence FLOAT,
    PRIMARY KEY (time, field_id, resolution)
);
SELECT create_hypertable('kriging_grids', 'time', 
                       chunk_time_interval => INTERVAL '7 days');
```

**Standard PostgreSQL Tables:**

```sql
-- Compliance ledger (immutable, hash-chained)
CREATE TABLE compliance_ledger (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    field_id UUID REFERENCES fields(id),
    event_time TIMESTAMPTZ NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB NOT NULL,
    previous_hash VARCHAR(64) NOT NULL,
    block_hash VARCHAR(64) NOT NULL,
    pbft_signatures JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_compliance_field_time ON compliance_ledger(field_id, event_time);

-- Field registry
CREATE TABLE fields (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    owner_id UUID REFERENCES users(id),
    geometry GEOGRAPHY(POLYGON, 4326) NOT NULL,
    center GEOGRAPHY(POINT, 4326),
    area_acres DECIMAL(8, 2),
    soil_type VARCHAR(50),
    water_district VARCHAR(50),
    sfd_configuration VARCHAR(50),  -- SFD-STD-126, etc.
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_fields_geometry ON fields USING GIST(geometry);
CREATE INDEX idx_fields_owner ON fields(owner_id);

-- Device registry
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_code VARCHAR(10) NOT NULL,  -- PMT, VFA, LRZB, etc.
    serial_number VARCHAR(50) UNIQUE NOT NULL,
    field_id UUID REFERENCES fields(id),
    activation_date TIMESTAMPTZ,
    firmware_version VARCHAR(20),
    last_seen TIMESTAMPTZ,
    battery_level FLOAT,
    status VARCHAR(20) DEFAULT 'inactive'
);
```

### 2.4 S3 Data Lake

**Bucket Structure:**

```
s3://farmsense-data/
├── raw-telemetry/
│   └── year=2026/
│       └── month=03/
│           └── day=19/
│               └── rss-slvalley-001/
│                   └── batch-001.json.gz
├── kriging-grids/
│   └── 1m/
│       └── field-uuid/
│           └── 2026-03-19-120000.tif
├── compliance-ledgers/
│   └── field-uuid/
│       └── 2026-Q1.dwr
└── ml-models/
    └── lstm-vwc-predictor/
        └── v2.3.1/
            └── model.pkl
```

**Lifecycle Policies:**

| Storage Class | Transition | Purpose |
|---------------|------------|---------|
| **Standard** | 0-30 days | Hot data, real-time access |
| **Infrequent Access** | 30-90 days | Warm data, dashboard |
| **Glacier Instant** | 90 days-2 years | Cold data, compliance |
| **Glacier Deep** | 2-7 years | Archive, Water Court |
| **Delete** | >7 years | Regulatory limit |

---

## 3. API Services

### 3.1 REST API (FastAPI)

**Authentication:**

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

app = FastAPI()
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            credentials.credentials,
            key=JWT_PUBLIC_KEY,
            algorithms=["RS256"]
        )
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/v1/fields/{field_id}/moisture")
async def get_field_moisture(
    field_id: str,
    depth: str = "30cm",
    resolution: str = "10m",
    token: dict = Depends(verify_token)
):
    # Verify field ownership
    if not owns_field(token["sub"], field_id):
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Query Kriging grid
    grid = await fetch_kriging_grid(field_id, depth, resolution)
    
    return {
        "field_id": field_id,
        "depth": depth,
        "resolution": resolution,
        "timestamp": grid.timestamp,
        "grid": grid.to_geojson(),
        "statistics": grid.compute_statistics()
    }
```

**Core Endpoints:**

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/v1/auth/login` | POST | JWT token issuance | Password |
| `/v1/fields` | GET | List user's fields | JWT |
| `/v1/fields/{id}/moisture` | GET | Current moisture grid | JWT |
| `/v1/fields/{id}/history` | GET | Time-series data | JWT |
| `/v1/fields/{id}/worksheet` | POST | Generate irrigation worksheet | JWT |
| `/v1/ingest/telemetry` | POST | RSS data ingestion | mTLS |
| `/v1/compliance/export` | GET | DWR export | JWT + 2FA |
| `/v1/admin/devices` | GET | Device management | Admin JWT |

### 3.2 WebSocket Real-Time

**Connection Management:**

```python
from fastapi import WebSocket
import asyncio

class FieldStream:
    def __init__(self):
        self.connections = {}  # field_id -> [websockets]
    
    async def connect(self, websocket: WebSocket, field_id: str):
        await websocket.accept()
        if field_id not in self.connections:
            self.connections[field_id] = []
        self.connections[field_id].append(websocket)
    
    async def broadcast(self, field_id: str, message: dict):
        if field_id in self.connections:
            dead_connections = []
            for ws in self.connections[field_id]:
                try:
                    await ws.send_json(message)
                except:
                    dead_connections.append(ws)
            
            # Clean up dead connections
            for ws in dead_connections:
                self.connections[field_id].remove(ws)
    
    async def handle_ingest(self, field_id: str, data: dict):
        """Called when new telemetry arrives"""
        await self.broadcast(field_id, {
            "type": "moisture_update",
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        })

@app.websocket("/v1/stream/field/{field_id}")
async def field_websocket(websocket: WebSocket, field_id: str):
    await field_stream.connect(websocket, field_id)
    try:
        while True:
            # Keep connection alive, handle pings
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except:
        await websocket.close()
```

### 3.3 GraphQL (Optional)

For complex, nested queries:

```graphql
type Field {
  id: ID!
  name: String!
  areaAcres: Float!
  moistureGrid(resolution: GridResolution!, depth: Depth!): MoistureGrid!
  devices: [Device!]!
  complianceHistory(start: DateTime!, end: DateTime!): [ComplianceEvent!]!
}

type MoistureGrid {
  timestamp: DateTime!
  resolution: GridResolution!
  cells: [GridCell!]!
  meanVWC: Float!
  minVWC: Float!
  maxVWC: Float!
}

type GridCell {
  lat: Float!
  lon: Float!
  vwc: Float!
  confidence: Float!
}

query GetFieldDashboard($fieldId: ID!) {
  field(id: $fieldId) {
    name
    moistureGrid(resolution: TEN_METER, depth: THIRTY_CM) {
      meanVWC
      cells(limit: 100) {
        lat
        lon
        vwc
      }
    }
    devices {
      code
      status
      lastSeen
      batteryLevel
    }
  }
}
```

---

## 4. Machine Learning Pipeline

### 4.1 LSTM Forecasting Model

**Architecture:**

```python
import torch
import torch.nn as nn

class VWC_Forecaster(nn.Module):
    def __init__(self, input_dim=6, hidden_dim=128, num_layers=2, output_dim=4):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2
        )
        self.fc = nn.Linear(hidden_dim, output_dim)
    
    def forward(self, x):
        # x: [batch, seq_len, features]
        # features: [vwc, temp, et, rain, solar, wind]
        lstm_out, _ = self.lstm(x)
        # Take last timestep
        last_hidden = lstm_out[:, -1, :]
        output = self.fc(last_hidden)
        # output: [batch, 4] -> VWC at 8", 16", 24", 36"
        return output

# Training configuration
hyperparameters = {
    "sequence_length": 168,  # 7 days of hourly data
    "prediction_horizon": 72,  # 3 days ahead
    "hidden_dim": 128,
    "num_layers": 2,
    "dropout": 0.2,
    "learning_rate": 0.001,
    "batch_size": 64,
    "epochs": 100
}
```

**Training Pipeline:**

```python
# SageMaker training job
from sagemaker.pytorch import PyTorch

estimator = PyTorch(
    entry_point="train.py",
    role=sagemaker_role,
    instance_type="ml.m5.2xlarge",
    instance_count=1,
    framework_version="2.0",
    py_version="py310",
    hyperparameters=hyperparameters
)

estimator.fit("s3://farmsense-data/ml-training/")

# Model deployment
predictor = estimator.deploy(
    initial_instance_count=2,
    instance_type="ml.c5.xlarge",
    endpoint_name="vwc-forecaster-v2-3"
)
```

**Feature Engineering:**

| Feature | Source | Transformation |
|---------|--------|----------------|
| **VWC history** | Sensor telemetry | Lagged values (t-24h, t-48h, t-168h) |
| **Soil temperature** | VFA sensors | Rolling mean (24h) |
| **ET₀** | Weather API | Daily reference ET |
| **Precipitation** | Radar + ground | Accumulated (24h, 72h) |
| **Solar radiation** | Satellite | Daily integral |
| **Wind speed** | Weather stations | Daily average |

### 4.2 Kriging Model Optimization

**Variogram Auto-Tuning:**

```python
from pykrige import OrdinaryKriging
from scipy.optimize import minimize

def optimize_variogram(sensor_data):
    """
    Auto-tune variogram parameters per field
    """
    def objective(params):
        nugget, sill, range_m = params
        try:
            ok = OrdinaryKriging(
                sensor_data['x'], sensor_data['y'], sensor_data['vwc'],
                variogram_model='spherical',
                variogram_parameters={'nugget': nugget, 'sill': sill, 'range': range_m}
            )
            # Cross-validation
            cv_errors = ok.cross_validation(n_splits=5)
            mse = np.mean(cv_errors**2)
            return mse
        except:
            return 1e6  # Large penalty for invalid params
    
    # Initial guess from regional defaults
    initial = [0.001, 0.008, 245]
    bounds = [(0, 0.01), (0.001, 0.1), (50, 1000)]
    
    result = minimize(objective, initial, bounds=bounds, method='L-BFGS-B')
    
    return {
        'nugget': result.x[0],
        'sill': result.x[1],
        'range': result.x[2],
        'mse': result.fun
    }
```

---

## 5. Security & Compliance

### 5.1 Identity & Access Management

**AWS IAM Structure:**

```yaml
# Service roles
roles:
  - name: eks-cluster-role
    trust: eks.amazonaws.com
    policies:
      - AmazonEKSClusterPolicy
  
  - name: telemetry-ingest-role
    trust: lambda.amazonaws.com
    policies:
      - s3:PutObject (raw-telemetry/*)
      - rds:Insert (sensor_telemetry)
  
  - name: farmer-user-role
    trust: cognito-identity.amazonaws.com
    policies:
      - rds:Select (owned fields only)
      - s3:GetObject (own compliance exports)

# Policy conditions
conditions:
  field_ownership: "rds:query WHERE owner_id = ${cognito:sub}"
  time_bound: "s3:presigned_url expires 1 hour"
```

**Multi-Factor Authentication:**

| Action | Required MFA |
|--------|--------------|
| Login | TOTP (Authy, Google) |
| Compliance export | TOTP + SMS backup |
| Admin actions | Hardware token (YubiKey) |
| API key generation | Hardware token |

### 5.2 Encryption

| Layer | Method | Key |
|-------|--------|-----|
| **In transit** | TLS 1.3 | AWS Certificate Manager |
| **At rest (RDS)** | AES-256 | AWS KMS (automatic) |
| **At rest (S3)** | SSE-KMS | Customer-managed key |
| **Backups** | AES-256 | AWS Backup encryption |
| **API secrets** | Sealed Secrets | Cluster-specific |

### 5.3 Compliance Certifications

| Standard | Status | Scope |
|----------|--------|-------|
| **SOC 2 Type II** | In progress | Security, availability |
| **ISO 27001** | Planned | Information security |
| **FedRAMP** | Evaluating | Federal deployments |
| **GDPR** | Compliant | EU data subjects |
| **CCPA** | Compliant | California residents |

---

## 6. Disaster Recovery

### 6.1 Backup Strategy

| Data | Frequency | Retention | Method |
|------|-----------|-----------|--------|
| **RDS** | Daily + continuous | 35 days | Automated snapshots |
| **S3** | Real-time (versioning) | 7 years | Cross-region replication |
| **EKS** | Infrastructure as Code | N/A | Terraform state |
| **Secrets** | Manual rotation | 90 days | AWS Secrets Manager |

### 6.2 Failover Procedures

**RDS Failover:**

1. **Detection**: CloudWatch alarm on primary latency
2. **Promotion**: Automatic read replica promotion
3. **DNS Update**: Route53 health check failover
4. **RTO**: 15 minutes
5. **RPO**: 5 minutes (async replication lag)

**Regional Failover:**

1. **Trigger**: us-west-2 unavailable
2. **Activation**: Manual decision (CEO/CTO approval)
3. **DNS Flip**: Route53 to us-east-1
4. **Data Sync**: Last 5 minutes from S3 replication
5. **RTO**: 30 minutes
6. **RPO**: 5 minutes

---

## 7. Cost Optimization

### 7.1 Monthly Cost Estimate (Production)

| Service | Configuration | Monthly Cost |
|---------|---------------|--------------|
| **EKS** | 3× m6i.2xlarge | $720 |
| **RDS** | db.r6g.2xlarge Multi-AZ | $1,200 |
| **ElastiCache** | cache.r6g.large | $180 |
| **S3** | 10TB with tiering | $400 |
| **CloudFront** | 1TB transfer | $100 |
| **SageMaker** | Training + inference | $500 |
| **Data transfer** | Cross-region | $200 |
| **Support** | Business tier | $800 |
| **TOTAL** | | **$4,100/month** |

**Per-Field Cost:** ~$3/month (1,280 fields in SLV)

### 7.2 Reserved Capacity

| Service | Commitment | Savings |
|---------|------------|---------|
| **EC2 (EKS)** | 1-year | 40% |
| **RDS** | 1-year | 45% |
| **Savings Plan** | Compute | 20-50% |

---

## 8. Revision History

| Version | Date | Author | Changes | Approval |
|---------|------|--------|---------|----------|
| 1.0 | 2025-01-10 | J. Beebe | Initial cloud architecture | Approved |
| 1.5 | 2025-07-20 | J. Beebe | Added SageMaker, DR procedures | Approved |
| 2.0 | 2026-03-19 | J. Beebe | Expanded security, compliance, cost | **PENDING** |

---

*Proprietary IP of bxthre3 inc. — Confidential*

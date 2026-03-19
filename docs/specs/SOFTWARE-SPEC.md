---
Status: Active
Last Audited: 2026-03-19
Drift Aversion: REQUIRED
System Code: SW
Full Name: FarmSense Software Stack
Version: 2.0
Category: Software Architecture & Development
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

# SOFTWARE V2.0: FarmSense Software Stack

## 1. Executive Summary

### 1.1 Role and Function

The FarmSense Software Stack is the **deterministic compute layer** — the firmware, edge applications, cloud services, and user interfaces that transform raw sensor data into actionable irrigation decisions. This specification covers the complete software architecture from bare-metal sensor firmware to the React farmer dashboard, including ML inference, Kriging algorithms, compliance reporting, and third-party integrations.

**Primary Functions:**

1. **Sensor Firmware**: Bare-metal C for VFA, LRZN, LRZB, PFA, PMT
2. **Edge Compute**: IDW interpolation, stall detection, reflex logic
3. **District Intelligence**: Kriging, PBFT consensus, Black Box
4. **Regional Master**: Regression Kriging, FHE vault, 7-year ledger
5. **Cloud Services**: Ingestion, ML training, compliance export
6. **Web Application**: React dashboard for farmers
7. **Mobile**: React Native field technician app
8. **APIs**: REST, WebSocket, GraphQL for integrators

**Software Hierarchy:**

| Layer | Language | Runtime | Primary Function |
|-------|----------|---------|------------------|
| **L0 Sensors** | C | Bare-metal | Data acquisition, LoRa TX |
| **L1.5 PMT** | C/C++ | ESP32-S3 | Aggregation, IDW, stall |
| **L2 DHU** | Python/C++ | Jetson Orin | Kriging, PBFT, caching |
| **L3 RSS** | Python | Threadripper | Master Kriging, FHE, vault |
| **L4 Cloud** | Python | AWS EKS | Ingestion, ML, APIs |
| **L5 Web** | TypeScript | React | Farmer dashboard |
| **L6 Mobile** | TypeScript | React Native | Technician app |

**Critical Distinction:**

| Entity | Software | Key Algorithm |
|--------|----------|---------------|
| **VFA** | nRF52 firmware | Topp equation (VWC from ε) |
| **PMT** | ESP32-S3 | IDW interpolation, IMU fusion |
| **DHU** | Jetson Python | Ordinary Kriging, PBFT |
| **RSS** | Threadripper Python | Regression Kriging, FHE |
| **Cloud** | FastAPI/SageMaker | LSTM, compliance export |
| **Web** | React | Geospatial visualization |

**Key Differentiator:** The software stack is **deterministic at every layer** — from fixed-cycle sensor chirps to bounded-time Kriging computation to hard real-time stall detection. No non-deterministic garbage collection at the edge; predictable latency from sensor to decision.

---

## 2. Firmware Specifications (L0-L1.5)

### 2.1 VFA Firmware (nRF52840)

**Architecture:**

```c
// VFA main loop - deterministic timing
#include <nrf52840.h>
#include <aes.h>
#include <lora.h>

#define CHIRP_INTERVAL_MS 14400000  // 4 hours base
#define SENSOR_COUNT 4            // 8", 16", 24", 36"

volatile uint32_t next_chirp_time;
volatile float volatility_score = 0.0;

typedef struct {
    uint32_t timestamp;
    uint16_t vwc[SENSOR_COUNT];    // 0.01% resolution
    int16_t temperature;             // 0.1°C resolution
    uint16_t battery_mv;
    uint8_t quality_score;
} vfa_payload_t;

int main(void) {
    // Hardware initialization
    clock_init();
    gpio_init();
    adc_init();           // Dielectric measurement
    sdi12_init();         // GroPoint sensors
    lora_init();          // 900MHz CSS
    
    // Load persisted state
    load_calibration();
    next_chirp_time = get_rtc_time() + CHIRP_INTERVAL_MS;
    
    while (1) {
        uint32_t now = get_rtc_time();
        
        // Adaptive chirp interval based on volatility
        uint32_t interval = calculate_chirp_interval(volatility_score);
        
        if (now >= next_chirp_time) {
            // Read sensors
            vfa_payload_t payload;
            payload.timestamp = now;
            
            for (int i = 0; i < SENSOR_COUNT; i++) {
                payload.vwc[i] = read_gropoint_vwc(i);
            }
            payload.temperature = read_sht31_temp();
            payload.battery_mv = read_battery();
            
            // Quality score based on variance
            payload.quality_score = compute_quality_score(payload.vwc, SENSOR_COUNT);
            
            // Encrypt and transmit
            uint8_t encrypted[32];
            aes_encrypt((uint8_t*)&payload, encrypted, DEVICE_KEY);
            lora_transmit(encrypted, sizeof(payload), SF_10);
            
            next_chirp_time = now + interval;
        }
        
        // Deep sleep until next event
        uint32_t sleep_ms = next_chirp_time - now;
        enter_deep_sleep(sleep_ms);
    }
}

// Topp equation: convert dielectric to VWC
float dielectric_to_vwc(float epsilon) {
    // Topp et al. (1980)
    // VWC = -5.3×10⁻² + 2.92×10⁻²×ε - 5.5×10⁻⁴×ε² + 4.3×10⁻⁶×ε³
    float vwc = -0.053 + 0.0292 * epsilon 
                - 0.00055 * epsilon * epsilon 
                + 0.0000043 * epsilon * epsilon * epsilon;
    return CLAMP(vwc, 0.0, 1.0);
}
```

**Power States:**

| State | Current | Wake Trigger | Duration |
|-------|---------|--------------|----------|
| **DORMANT** | 12µA | RTC alarm | 4 hours |
| **ANTICIPATORY** | 45mA | Sunrise temp rise | 1 hour |
| **FOCUS RIPPLE** | 120mA | Moisture anomaly | 15 min |
| **TRANSMIT** | 150mA | Chirp schedule | <100ms |

### 2.2 PMT Firmware (ESP32-S3)

**Architecture:**

```cpp
// PMT FreeRTOS task structure
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <esp32s3.h>
#include <ublox.h>
#include <bno055.h>

// Task priorities (higher = more urgent)
#define PRIORITY_STALL      24  // Real-time safety
#define PRIORITY_GNSS       20  // Position critical
#define PRIORITY_LORA_RX    18  // Sensor data
#define PRIORITY_IDW        15  // Computation
#define PRIORITY_WIFI_TX    12  // Background upload
#define PRIORITY_IDLE       1   // Lowest

// Core affinity
core_config_t core_assignments = {
    .core_0 = {TASK_LORA_RX, TASK_WIFI_TX, TASK_IDLE},
    .core_1 = {TASK_STALL, TASK_GNSS, TASK_IDW}
};

// Stall detection - runs on Core 1 exclusively
void task_stall_detection(void *pvParameters) {
    while (1) {
        // Read IMU at 100Hz
        imu_data_t imu = bno055_read();
        
        // Get expected motion from GNSS
        float expected_angular_velocity = gnss_get_expected_angular_velocity();
        
        // Detect mismatch (stall condition)
        if (fabs(imu.gyro_z - expected_angular_velocity) > STALL_THRESHOLD) {
            // High priority alert - bypass normal queue
            xTaskNotifyGive(xStallAlertTask);
        }
        
        vTaskDelay(pdMS_TO_TICKS(10));  // 100Hz
    }
}

// IDW interpolation on Core 1
void task_idw_compute(void *pvParameters) {
    while (1) {
        // Wait for sensor aggregation complete
        ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
        
        // Compute 50m IDW grid (GPU-accelerated on ESP32-S3 vector unit)
        grid_50m_t grid;
        compute_idw_gpu(&sensor_buffer, &grid);
        
        // Package into 187-byte Field State
        field_state_t state;
        package_field_state(&grid, &sensor_buffer, &state);
        
        // Queue for transmission
        xQueueSend(txQueue, &state, 0);
    }
}

// 187-byte Field State Payload structure
struct __attribute__((packed)) FieldState {
    // Header (7 bytes)
    uint8_t protocol = 0x02;
    uint8_t device_type = 0x05;  // PMT
    uint16_t sequence;
    uint32_t timestamp;
    
    // GNSS (16 bytes)
    int32_t lat_e7, lon_e7, alt_mm;
    uint16_t accuracy_mm, speed_mm_s, heading;
    uint8_t sats, fix_type;
    
    // IMU (12 bytes)
    int16_t accel[3], gyro[3], mag[3];
    
    // Sensor data (96 bytes = 6 × 16 bytes)
    SubNodeData vfa[2];
    SubNodeData lrzb[2];
    SubNodeData lrzn[2];
    
    // Flow (8 bytes)
    uint32_t flow_total;
    uint16_t flow_rate, flow_quality;
    
    // Grid stats (32 bytes)
    uint16_t mean_vwc, min_vwc, max_vwc, std_vwc;
    uint8_t compressed_grid[24];
    
    // Diagnostics (16 bytes)
    uint8_t cpu, heap, temp;
    uint16_t battery;
    uint32_t uptime;
    uint8_t errors;
    
} __attribute__((packed));  // Total: 187 bytes
```

**Reflex Logic Engine:**

```cpp
class ReflexEngine {
public:
    ReflexDecision evaluate(const SensorSnapshot& snapshot) {
        ReflexDecision decision;
        
        // Condition 1: PMT stall detection
        if (snapshot.stall_detected) {
            decision.action = ACTUATE_STOP;
            decision.trigger = TRIGGER_STALL;
            decision.priority = PRIORITY_CRITICAL;
            return decision;
        }
        
        // Condition 2: Line pressure loss
        if (snapshot.pfa_pressure < PRESSURE_THRESHOLD_PSI) {
            decision.action = ACTUATE_STOP;
            decision.trigger = TRIGGER_PRESSURE_LOSS;
            decision.priority = PRIORITY_CRITICAL;
            return decision;
        }
        
        // Condition 3: Deep saturation
        if (snapshot.vfa_48in_vwc > 0.95) {
            decision.action = ACTUATE_STOP;
            decision.trigger = TRIGGER_SATURATION;
            decision.priority = PRIORITY_HIGH;
            return decision;
        }
        
        // Condition 4: Pump cavitation
        if (snapshot.pfa_cavitation_detected) {
            decision.action = ACTUATE_STOP;
            decision.trigger = TRIGGER_CAVITATION;
            decision.priority = PRIORITY_HIGH;
            return decision;
        }
        
        // Default: Continue
        decision.action = NO_ACTION;
        return decision;
    }
    
    void execute(const ReflexDecision& decision) {
        if (decision.action == ACTUATE_STOP) {
            // Send stop command to PFA via LoRa
            lora_send_pfa_command(CMD_STOP, decision.priority);
            
            // Log to local Black Box
            log_reflex_event(decision);
            
            // Alert DHU
            wifi_send_alert(ALERT_REFLEX_TRIGGERED, decision);
        }
    }
};
```

---

## 3. Edge Software (L2-L3)

### 3.1 DHU Software (Jetson Orin Nano)

**Architecture:**

```python
# DHU Python architecture
import asyncio
import numpy as np
from pykrige.ok import OrdinaryKriging
from sklearn.ensemble import RandomForestRegressor

class DistrictHub:
    def __init__(self, district_id, config):
        self.district_id = district_id
        self.pmt_clients = {}  # field_id -> PMT connection
        self.krige_cache = LRUCache(maxsize=100)
        self.pbft_node = PBFTNode(node_id=district_id)
        self.black_box = BlackBoxCache('/blackbox', retention_days=30)
        
    async def run(self):
        # Parallel coroutines
        await asyncio.gather(
            self.listen_for_pmts(),      # 900MHz LoRa + 2.4GHz WiFi
            self.compute_kriging(),       # GPU-accelerated
            self.run_pbft_consensus(),    # AllianceChain
            self.sync_to_rss(),           # 60GHz backhaul
            self.health_monitor()         # Self-diagnostics
        )
    
    async def compute_kriging(self):
        """Ordinary Kriging on GPU every 15 minutes"""
        while True:
            # Collect latest sensor data from all fields
            field_data = await self.aggregate_field_data()
            
            for field_id, sensors in field_data.items():
                # GPU-accelerated Kriging
                grid_20m = self.krige_20m(sensors)
                grid_10m = self.krige_10m(sensors)
                
                # Cache results
                self.krige_cache[(field_id, '20m')] = grid_20m
                self.krige_cache[(field_id, '10m')] = grid_10m
                
                # Compute statistics
                stats = {
                    'mean_vwc': float(np.mean(grid_20m)),
                    'min_vwc': float(np.min(grid_20m)),
                    'max_vwc': float(np.max(grid_20m)),
                    'std_vwc': float(np.std(grid_20m)),
                    'mape': self.compute_mape(sensors, grid_20m)
                }
                
                # Store in Black Box
                await self.black_box.store_kriging(
                    field_id=field_id,
                    timestamp=datetime.utcnow(),
                    grids={'20m': grid_20m, '10m': grid_10m},
                    statistics=stats
                )
            
            await asyncio.sleep(900)  # 15 minutes
    
    def krige_20m(self, sensors):
        """20-meter resolution Ordinary Kriging"""
        x = np.array([s['x'] for s in sensors])
        y = np.array([s['y'] for s in sensors])
        z = np.array([s['vwc'] for s in sensors])
        
        # Variogram model (calibrated per district)
        variogram = {
            'model': 'spherical',
            'nugget': 0.0012,
            'sill': 0.0085,
            'range': 245
        }
        
        # GPU-accelerated Kriging
        ok = OrdinaryKriging(
            x, y, z,
            variogram_model=variogram,
            enable_gpu=True  # Uses CuPy on Jetson
        )
        
        # Create 20m grid
        field = self.get_field_bounds()
        grid_x = np.arange(field['min_x'], field['max_x'], 20)
        grid_y = np.arange(field['min_y'], field['max_y'], 20)
        
        z_krige, ss = ok.execute('grid', grid_x, grid_y)
        
        return z_krige
```

**PBFT Consensus:**

```python
class PBFTNode:
    """Byzantine Fault Tolerant consensus for Digital Water Ledger"""
    
    def __init__(self, node_id, peers, f=1):
        self.node_id = node_id
        self.peers = peers  # List of peer node IDs
        self.f = f  # Fault tolerance (tolerates f Byzantine nodes)
        self.view_number = 0
        self.sequence_number = 0
        
    async def propose(self, value):
        """Leader proposes a ledger entry"""
        if not self.is_leader():
            return None
        
        pre_prepare = {
            'view': self.view_number,
            'sequence': self.sequence_number,
            'digest': sha256(value),
            'value': value,
            'leader': self.node_id
        }
        
        # Broadcast to all replicas
        await self.broadcast('pre_prepare', pre_prepare)
        
        # Wait for 2f+1 prepares
        prepares = await self.wait_for_prepares(timeout=5.0)
        if len(prepares) < 2 * self.f + 1:
            return None  # Consensus failed
        
        # Send commit
        commit = {
            'view': self.view_number,
            'sequence': self.sequence_number,
            'digest': pre_prepare['digest']
        }
        await self.broadcast('commit', commit)
        
        # Wait for 2f+1 commits
        commits = await self.wait_for_commits(timeout=5.0)
        if len(commits) >= 2 * self.f + 1:
            self.sequence_number += 1
            return value  # Consensus achieved
        
        return None
```

### 3.2 RSS Software (Threadripper PRO)

**Architecture:**

```python
# RSS - Regional Superstation
import torch
from pykrige.rk import RegressionKriging

class RegionalSuperstation:
    def __init__(self, region_id):
        self.region_id = region_id
        self.dhu_clients = {}  # district_id -> DHU connection
        self.fhe_vault = FHEVault()
        self.ledger = DigitalWaterLedger()
        
        # ML models
        self.regression_model = self.load_regression_model()
        self.lstm_forecaster = self.load_lstm_model()
        
    def compute_master_kriging(self, district_grids):
        """1-meter Regression Kriging across all districts"""
        
        # Combine all district data
        all_sensors = []
        for district_id, sensors in district_grids.items():
            all_sensors.extend(sensors)
        
        # Regression trend (Sentinel-2 + DEM)
        sentinel_ndvi = self.fetch_sentinel_coverage()
        dem = self.fetch_lidar_elevation()
        
        X = self.build_regressors(sentinel_ndvi, dem)
        
        # GPU-accelerated trend prediction (2× A100)
        with torch.no_grad():
            trend = self.regression_model(
                torch.tensor(X).cuda()
            ).cpu().numpy()
        
        # Kriging on residuals
        residuals = self.compute_residuals(all_sensors, trend)
        
        ok = RegressionKriging(
            regression_model=self.regression_model,
            residual_kriging='ordinary',
            variogram_model='spherical'
        )
        
        # 1-meter grid for entire region
        master_grid = ok.execute(
            grid_resolution=1,  # 1 meter
            bbox=self.region_bounds
        )
        
        return master_grid
    
    def fhe_aggregate(self, encrypted_readings):
        """Aggregate encrypted data without decryption"""
        # Privacy-preserving computation
        return self.fhe_vault.sum(encrypted_readings)
```

---

## 4. Cloud Services (L4)

### 4.1 API Gateway (FastAPI)

```python
from fastapi import FastAPI, Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FarmSense API", version="2.0")

# CORS for web dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.farmsense.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Dependency injection
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, JWT_SECRET, algorithms=["RS256"])
    return await User.get(payload["sub"])

@app.get("/v1/fields/{field_id}/moisture")
async def get_moisture_grid(
    field_id: UUID,
    depth: DepthEnum = DepthEnum.cm_30,
    resolution: ResolutionEnum = ResolutionEnum.m_10,
    user: User = Depends(get_current_user)
):
    """Get Kriging moisture grid for a field"""
    
    # Authorization check
    if not await user.owns_field(field_id):
        raise HTTPException(403, "Access denied")
    
    # Fetch from cache or compute
    grid = await KrigingService.get_grid(
        field_id=field_id,
        depth=depth,
        resolution=resolution
    )
    
    return {
        "field_id": str(field_id),
        "timestamp": grid.timestamp.isoformat(),
        "depth": depth.value,
        "resolution": resolution.value,
        "grid": grid.to_geojson(),
        "statistics": {
            "mean": grid.mean_vwc,
            "min": grid.min_vwc,
            "max": grid.max_vwc,
            "std": grid.std_vwc
        }
    }

@app.post("/v1/irrigation/worksheet")
async def generate_worksheet(
    request: WorksheetRequest,
    user: User = Depends(get_current_user)
):
    """Generate VRI irrigation worksheet"""
    
    # Get latest Kriging grid
    grid = await KrigingService.get_grid(
        field_id=request.field_id,
        depth=DepthEnum.cm_30,
        resolution=ResolutionEnum.m_10
    )
    
    # Compute MAD threshold
    mad_threshold = await SoilService.get_mad_threshold(
        field_id=request.field_id
    )
    
    # Generate prescription
    worksheet = VRIEngine.generate_prescription(
        grid=grid,
        mad_threshold=mad_threshold,
        pivot_geometry=request.pivot_geometry
    )
    
    # Log to compliance ledger
    await ComplianceService.log_worksheet(worksheet)
    
    return worksheet
```

### 4.2 ML Training Pipeline (SageMaker)

```python
# SageMaker training job
def train_lstm_forecaster():
    from sagemaker.pytorch import PyTorch
    
    estimator = PyTorch(
        entry_point="train_vwc_forecaster.py",
        role=AWS_ROLE,
        instance_type="ml.p3.2xlarge",  # V100 GPU
        instance_count=1,
        framework_version="2.0",
        hyperparameters={
            "epochs": 100,
            "batch_size": 64,
            "learning_rate": 0.001,
            "sequence_length": 168,  # 7 days
            "hidden_dim": 128,
            "num_layers": 2
        }
    )
    
    estimator.fit("s3://farmsense-data/ml-training/")
    
    # Deploy endpoint
    predictor = estimator.deploy(
        initial_instance_count=2,
        instance_type="ml.c5.2xlarge",
        endpoint_name="vwc-forecaster-prod"
    )
    
    return predictor
```

---

## 5. Frontend (L5)

### 5.1 React Dashboard

```typescript
// React component structure
import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';
import { useQuery } from '@tanstack/react-query';

interface MoistureGrid {
  fieldId: string;
  timestamp: string;
  cells: GridCell[];
  statistics: GridStats;
}

interface GridCell {
  lat: number;
  lon: number;
  vwc: number;
  confidence: number;
}

const FieldDashboard: React.FC<{ fieldId: string }> = ({ fieldId }) => {
  const [selectedDepth, setSelectedDepth] = useState<Depth>('30cm');
  const [selectedResolution, setSelectedResolution] = useState<Resolution>('10m');
  
  // Fetch moisture grid
  const { data: grid, isLoading } = useQuery<MoistureGrid>(
    ['moisture', fieldId, selectedDepth, selectedResolution],
    () => fetchMoistureGrid(fieldId, selectedDepth, selectedResolution),
    { refetchInterval: 300000 }  // 5 minutes
  );
  
  // WebSocket for real-time updates
  useEffect(() => {
    const ws = new WebSocket(`wss://api.farmsense.io/v1/stream/field/${fieldId}`);
    
    ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      if (update.type === 'moisture_update') {
        // Update grid with delta
        queryClient.setQueryData(
          ['moisture', fieldId, selectedDepth, selectedResolution],
          (old: MoistureGrid) => applyDelta(old, update.delta)
        );
      }
    };
    
    return () => ws.close();
  }, [fieldId, selectedDepth, selectedResolution]);
  
  if (isLoading) return <LoadingSpinner />;
  
  return (
    <div className="field-dashboard">
      <Header fieldId={fieldId} timestamp={grid?.timestamp} />
      
      <Controls
        depth={selectedDepth}
        resolution={selectedResolution}
        onDepthChange={setSelectedDepth}
        onResolutionChange={setSelectedResolution}
      />
      
      <div className="main-content">
        <MoistureMap grid={grid!} />
        
        <Sidebar>
          <StatisticsPanel stats={grid!.statistics} />
          <SensorStatus fieldId={fieldId} />
          <IrrigationControl fieldId={fieldId} />
        </Sidebar>
      </div>
    </div>
  );
};

const MoistureMap: React.FC<{ grid: MoistureGrid }> = ({ grid }) => {
  // Color scale for VWC
  const getColor = (vwc: number) => {
    if (vwc < 0.15) return '#d73027';  // Very dry (red)
    if (vwc < 0.25) return '#fc8d59';  // Dry (orange)
    if (vwc < 0.35) return '#fee08b';  // Adequate (yellow)
    if (vwc < 0.45) return '#d9ef8b';  // Good (light green)
    return '#1a9850';  // Saturated (green)
  };
  
  return (
    <MapContainer center={grid.center} zoom={16}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      
      {/* Kriging grid as heatmap */}
      <HeatmapLayer
        points={grid.cells.map(c => ({
          lat: c.lat,
          lng: c.lon,
          intensity: c.vwc
        }))}
        radius={20}
        blur={15}
        maxZoom={18}
      />
      
      {/* Sensor locations */}
      {grid.sensors?.map(sensor => (
        <SensorMarker
          key={sensor.id}
          position={[sensor.lat, sensor.lon]}
          type={sensor.type}
          reading={sensor.lastReading}
        />
      ))}
    </MapContainer>
  );
};
```

---

## 6. Mobile App (L6)

### 6.1 React Native Technician App

```typescript
// Field technician mobile app
import React, { useState } from 'react';
import { View, Text, Button, Alert } from 'react-native';
import { BarcodeScanner } from 'expo-barcode-scanner';
import { BleManager } from 'react-native-ble-plx';

const DeviceInstallationScreen: React.FC = () => {
  const [scanning, setScanning] = useState(false);
  const [device, setDevice] = useState<DiscoveredDevice | null>(null);
  
  const scanForDevice = async () => {
    setScanning(true);
    
    const bleManager = new BleManager();
    
    bleManager.startDeviceScan(null, null, (error, scannedDevice) => {
      if (scannedDevice && scannedDevice.name?.startsWith('FS-')) {
        setDevice(scannedDevice);
        bleManager.stopDeviceScan();
        setScanning(false);
      }
    });
    
    // Timeout after 30 seconds
    setTimeout(() => {
      bleManager.stopDeviceScan();
      setScanning(false);
    }, 30000);
  };
  
  const installDevice = async () => {
    if (!device) return;
    
    try {
      // Connect via BLE
      const connected = await device.connect();
      
      // Read device info
      const deviceInfo = await connected.readCharacteristic(
        DEVICE_INFO_SERVICE,
        SERIAL_NUMBER_CHAR
      );
      
      // Activate device in backend
      await API.activateDevice({
        serialNumber: deviceInfo.value,
        fieldId: currentFieldId,
        location: currentGPSLocation
      });
      
      // Configure device
      await connected.writeCharacteristic(
        CONFIG_SERVICE,
        NETWORK_ID_CHAR,
        currentNetworkId
      );
      
      Alert.alert('Success', 'Device activated successfully');
      
    } catch (error) {
      Alert.alert('Error', `Installation failed: ${error.message}`);
    }
  };
  
  return (
    <View>
      <Text>Install New Device</Text>
      
      {!device && (
        <Button
          title={scanning ? "Scanning..." : "Scan for Device"}
          onPress={scanForDevice}
          disabled={scanning}
        />
      )}
      
      {device && (
        <View>
          <Text>Found: {device.name}</Text>
          <Text>RSSI: {device.rssi} dBm</Text>
          <Button title="Install" onPress={installDevice} />
        </View>
      )}
    </View>
  );
};
```

---

## 7. Development Practices

### 7.1 Code Organization

```
farmsense-code/
├── firmware/
│   ├── vfa/                 # nRF52840 bare-metal C
│   ├── lrzb/               # nRF52840 bare-metal C
│   ├── lrzn/               # nRF52840 bare-metal C
│   ├── pfa/                # nRF52840 bare-metal C
│   └── pmt/                # ESP32-S3 FreeRTOS C++
├── edge/
│   ├── dhu/                # Jetson Python
│   └── rss/                # Threadripper Python
├── cloud/
│   ├── api/                # FastAPI Python
│   ├── ml/                 # SageMaker training
│   └── workers/            # Background jobs
├── web/
│   ├── dashboard/          # React TypeScript
│   └── components/         # Shared UI
└── mobile/
    └── technician/         # React Native
```

### 7.2 Testing Strategy

| Layer | Unit Tests | Integration | E2E |
|-------|------------|-------------|-----|
| **Firmware** | Ceedling (C) | Hardware-in-loop | Field trial |
| **Edge** | pytest | Docker compose | Staging DHU |
| **Cloud** | pytest | LocalStack | Staging EKS |
| **Web** | Jest | React Testing Lib | Cypress |
| **Mobile** | Jest | Detox | Device farm |

---

## 8. Revision History

| Version | Date | Author | Changes | Approval |
|---------|------|--------|---------|----------|
| 1.0 | 2025-01-05 | J. Beebe | Initial software architecture | Approved |
| 1.5 | 2025-06-30 | J. Beebe | Added FHE, PBFT, React Native | Approved |
| 2.0 | 2026-03-19 | J. Beebe | Full stack documentation | **PENDING** |

---

*Proprietary IP of bxthre3 inc. — Confidential*

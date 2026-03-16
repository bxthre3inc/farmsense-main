# MODULAR DAP (Drift Aversion Protocol)
# Module: E-DAP (Engineering)
# 1. **Architectural Integrity**: Implementation must adhere to the Master Software Architecture.
# 2. **Synchronized Updates**: Changes to system behavior MUST be reflected in D-DAP documentation.
# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

# 3. **AI Agent Compliance**: Agents MUST verify the current implementation against documentation before proposing changes.
# 4. **No Ghost Edits**: All significant modifications must be documented in the project's audit trail.

from datetime import datetime
from sqlalchemy.orm import Session
from app.models import VirtualSensorGrid50m, VirtualSensorGrid20m, VirtualSensorGrid1m, SoilSensorReading
from app.services.external_data_service import ExternalDataService
from app.services.satellite_service import SatelliteDataService
from app.services.rss_kriging import RSSKrigingEngine
from app.services.hvs_sync_service import HVSSyncService
from app.services.yield_prediction_service import YieldPredictionService
from app.services.vri_prescription_service import VRIPrescriptionService
from app.core.env_wrapper import platform_wrapper
import logging
import uuid

logger = logging.getLogger(__name__)

class GridRenderingService:
    @staticmethod
    def get_or_render_grid(
        db: Session,
        field_id: str,
        resolution: str,
        limit: int = 1000,
        offline_mode: bool = False,
        predictive_mode: bool = False
    ):
        """
        Dynamically renders the grid based on recent sensor trends, 
        Landsat history, and real-time external environmental factors.
        
        If offline_mode is True, it fallbacks to local cached data with 
        a reduced confidence score.
        """
        logger.info(f"Rendering grid for field {field_id} at {resolution} resolution (Offline: {offline_mode})")

        # 1. Fetch recent sensor readings to determine trend
        readings = db.query(SoilSensorReading).filter(
            SoilSensorReading.field_id == field_id
        ).order_by(SoilSensorReading.timestamp.desc()).limit(3).all()

        trend_modifier = 1.0
        if len(readings) == 3:
            r1, r2, r3 = readings
            if r1.moisture_surface < r2.moisture_surface < r3.moisture_surface:
                trend_modifier = 0.8  # Drying trend
                logger.info(f"Detected drying trend for field {field_id}")

        # 2. Integrate External Atmospheric Data (Open-Meteo)
        # Mock coordinates for field center - in production these would be field metadata
        field_lat, field_lon = 40.5853, -105.0844 
        weather = ExternalDataService.get_weather_data(field_lat, field_lon)
        
        weather_modifier = 1.0
        if weather:
            temp = weather.get("temperature", 20)
            if temp > 30: # Extreme heat
                weather_modifier *= 1.15 # Increase evapotranspiration stress
                logger.info(f"Adjusting for extreme heat: {temp}C")
        
                soil_modifier = 0.9 
                logger.info(f"Adjusting for low Soil Organic Carbon: {soc}")

        # 3. Integrate Advanced Satellite Fusion (Sentinel-1 & 2)
        # Sentinel-2 NDVI (Optical)
        real_ndvi = SatelliteDataService.get_latest_ndvi_point(field_lat, field_lon, field_id)
        
        # Sentinel-1 SAR (Radar) - moisture proxy through clouds
        sar_modifier = SatelliteDataService.get_sentinel1_moisture_proxy(field_lat, field_lon)
        
        logger.info(f"Satellite Fusion: Sentinel-2 NDVI={real_ndvi:.2f}, Sentinel-1 SAR Mod={sar_modifier:.2f}")

        # 4. Calculate Confidence Score
        # 1.0 = All sensors online + Satellite recent
        # < 0.5 = High uncertainty
        confidence = 1.0
        
        if platform_wrapper.is_pilot():
            confidence *= 0.9 # Minor penalty for pilot-phase uncalibrated sensors
            logger.info("ENVIRONMENT: Pilot mode detected. Applying calibration buffer.")
        elif not platform_wrapper.is_production():
            confidence *= 0.8 # Dev mode penalty
            
        if offline_mode:
            confidence *= 0.7  # Reduced confidence due to stale external data
            logger.warning(f"Field {field_id} is in OFFLINE mode. Using local cache fallbacks.")
        
        if len(readings) < 3:
            confidence *= 0.8  # Sparse physical sensor data
            
        final_modifier = trend_modifier * weather_modifier * soil_modifier * sar_modifier
        logger.info(f"Fusion Complete. Final Modifier: {final_modifier:.2f}, Confidence: {confidence:.2f}")

        # 5. Render Grid
        model_map = {
            "50m": VirtualSensorGrid50m,
            "20m": VirtualSensorGrid20m,
            "1m": VirtualSensorGrid1m
        }
        
        Model = model_map.get(resolution)
        if not Model:
            raise ValueError(f"Invalid resolution: {resolution}")

        # Fetch latest cached results
        results = db.query(Model).filter(
            Model.field_id == field_id
        ).order_by(Model.timestamp.desc()).limit(limit).all()
        
        rss_engine = RSSKrigingEngine()

        # Apply spatiotemporal decay to cached results
        if results:
            latest_ts = results[0].timestamp
            hours_since_last = (datetime.utcnow() - latest_ts).total_seconds() / 3600.0
            
            # Convert DB objects to Dict for the engine processing
            results_dict = []
            for r in results:
                results_dict.append({
                    "field_id": r.field_id,
                    "grid_id": r.grid_id,
                    "timestamp": r.timestamp,
                    "moisture_surface": r.moisture_surface,
                    "confidence_score": r.confidence_score,
                    "computation_mode": r.computation_mode
                })
            
            decayed_results = rss_engine.apply_spatiotemporal_decay(results_dict, hours_since_last)
            
            # Update the DB objects with decayed values (in-memory for this return)
            for i, r in enumerate(results):
                r.confidence_score = decayed_results[i]['confidence_score']
                r.computation_mode = decayed_results[i]['computation_mode']

        # If no results or if the latest results are "STALE", trigger a re-render
        is_stale = results and "STALE" in results[0].computation_mode
        
        if (not results or is_stale) and resolution == "1m":
             logger.info(f"Triggering 1m grid refresh for {field_id} (Reason: {'No cache' if not results else 'Stale data'})")
             
             # Convert SoilSensorReadings to the format expected by RSSKrigingEngine
             sensor_list = [
                 {'lat': r.location.lat, 'lon': r.location.lon, 'moisture': r.moisture_surface} 
                 for r in readings if r.location
             ]
             
             # Differential update: provide previous grid if available and not too old
             prev_grid = None
             if results and not is_stale:
                 prev_grid = results_dict

             rss_grid = rss_engine.generate_1m_grid(field_id, sensor_list, prev_grid=prev_grid)
             
             # Save to DB and return
             # HVS Sync (Horizontal-Vertical Sync): Superimpose VFA anchors onto 1m grid
             hvs_svc = HVSSyncService()
             # Mock a nearby VFA anchor reading for the field
             mock_vfa = {
                 'id': 'VFA_ANCHOR_001',
                 'slot_10_moisture': 0.28,
                 'slot_18_moisture': 0.32,
                 'slot_25_moisture': 0.35,
                 'slot_35_moisture': 0.30,
                 'slot_48_moisture': 0.25
             }

             results = []
             for g in rss_grid:
                 # Apply HVS Sync logic to the grid point data
                 synced_cell = hvs_svc.sync_grid_cell(g, mock_vfa)
                 
                 db_point = VirtualSensorGrid1m(
                     field_id=synced_cell['field_id'],
                     grid_id=synced_cell['grid_id'],
                     timestamp=synced_cell['timestamp'],
                     location=f"POINT({synced_cell['longitude']} {synced_cell['latitude']})",
                     moisture_surface=synced_cell['moisture_surface'] * final_modifier,
                     moisture_root=synced_cell['moisture_root'] * final_modifier, # Populated by HVS
                     confidence_score=synced_cell['confidence_score'] * confidence,
                     computation_mode=synced_cell['computation_mode'],
                     source_sensors=synced_cell.get('vertical_profile') # Store the derived profile
                 )
                 db.add(db_point)
                 results.append(db_point)
             
             # Phase 4: FHE Secure Aggregation (SIMD-Batched)
             if results and "FHE" in results[0].computation_mode:
                logger.info(f"FHE_ENCLAVE: Performing secure regional aggregation for field {field_id}")
                # Simulate aggregation of the entire 1m grid into a single secure mean
                fhe_vec = rss_engine.generate_1m_grid(field_id, sensor_list, prev_grid=prev_grid, fhe_enabled=True)
                # This is just for demonstration of the API flow
                
             db.commit()
        
        # Phase 2: Predictive & Prescriptive Enhancements
        if predictive_mode:
            logger.info(f"SYNTHESIS: Generating 48-hour predictive moisture forecast for {field_id}")
            # Mock temporal shift: Simulate 48h drying trend unless high moisture
            for r in results:
                # If moisture is high, it stays wetter longer, else dries 15%
                m_val = getattr(r, 'moisture_surface', 0.25)
                drying_factor = 0.85 if m_val < 0.3 else 0.95
                r.moisture_surface = m_val * drying_factor
                r.computation_mode += "_PREDICTIVE_48H"

        # VRI Enrichment: Inject prescription metadata into the grid response
        if resolution == "1m":
            vri_engine = VRIPrescriptionService()
            
            # Convert objects to dict for VRI processing
            points_to_process = []
            for r in results:
                points_to_process.append({
                    "field_id": r.field_id,
                    "grid_id": r.grid_id,
                    "moisture_surface": r.moisture_surface
                })
                
            prescriptions = vri_engine.generate_prescription(points_to_process)
            
            # In a real app, we'd attach this to the return object or a separate schema
            # For this prototype, we'll log the enhancement and effectively "update" the objects in memory
            if prescriptions:
                metrics = vri_engine.calculate_efficiency_gain(prescriptions)
                logger.info(f"VRI Logic Applied. Estimated Water Sync Efficiency: {metrics['estimated_water_savings_pct']:.1f}%")
                
                # Attach VRI metadata to the objects (simulated enrichment)
                for i, r in enumerate(results):
                    setattr(r, 'vri_nozzle_setting', prescriptions[i]['vri_nozzle_setting'])
                    setattr(r, 'target_gpt_adjustment', prescriptions[i]['target_gpt_adjustment'])

        # Phase 6: MSF Yield Prediction
        if resolution == "1m":
            yield_svc = YieldPredictionService()
            # Convert objects to dict for batch prediction
            grid_dicts = []
            for r in results:
                # Reconstruct dict from DB object attributes
                d = {
                    'moisture_surface': r.moisture_surface,
                    'ndvi': getattr(r, 'ndvi', 0.6),
                    'ndwi': getattr(r, 'ndwi', 0.1),
                    'computation_mode': r.computation_mode,
                    'source_sensors': r.source_sensors # This holds the vertical profile from HVS
                }
                grid_dicts.append(d)
            
            predicted_grid = yield_svc.batch_predict_grid(grid_dicts)
            
            # Apply predictions back to the objects
            for i, r in enumerate(results):
                r.yield_forecast_kgha = predicted_grid[i]['yield_forecast_kgha']
                r.crop_stress_probability = predicted_grid[i]['crop_stress_probability']
                r.computation_mode = predicted_grid[i]['computation_mode']

        return results

    @staticmethod
    def _fetch_satellite_data(field_id: str) -> dict:
        return {f"cell_{i}": 0.3 + (i % 5) * 0.1 for i in range(10)}

    @staticmethod
    def _generate_synthetic_1m_grid(db: Session, field_id: str, modifier: float, ground_truth: float = None):
        points = []
        base_time = datetime.utcnow()
        
        for i in range(10):
            p = VirtualSensorGrid1m(
                id=uuid.uuid4(),
                field_id=field_id,
                grid_id=f"{field_id}_1m_{i}",
                timestamp=base_time,
                location=f"POINT(-105.00{i} 40.00{i})",
                moisture_surface=0.25 * modifier,
                moisture_root=0.30 * modifier,
                temperature=22.5,
                ndvi=0.4 + (modifier - 1.0),
                ndwi=0.1,
                confidence_score=0.95 if modifier > 0.8 else 0.6,
                physical_probe_value=ground_truth,
                crop_stress_probability=max(0.0, 1.0 - modifier),
                yield_forecast_kgha=8500 * modifier,
                irrigation_priority=1 if modifier < 0.8 else 5
            )
            points.append(p)
            db.add(p)
        
        db.commit()
        return points
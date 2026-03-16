import React, { useState } from 'react';
import Map, { NavigationControl, ScaleControl, Source, Layer, FullscreenControl } from 'react-map-gl/maplibre';
import 'maplibre-gl/dist/maplibre-gl.css';
import { Map as MapIcon, Layers, Crosshair, Radio, Globe, ShieldCheck, Activity, Info, X, Zap, ChevronRight, Filter } from 'lucide-react';

// Mock data for map layers
const mockSensors = {
    type: 'FeatureCollection',
    features: Array.from({ length: 50 }, (_, i) => ({
        type: 'Feature',
        id: i,
        properties: {
            id: `VFA-${100 + i}`,
            type: 'moisture',
            value: 0.25 + Math.random() * 0.2,
            status: Math.random() > 0.1 ? 'online' : 'offline',
            battery: 40 + Math.random() * 60
        },
        geometry: {
            type: 'Point',
            coordinates: [-106.132 + (Math.random() - 0.5) * 0.1, 37.485 + (Math.random() - 0.5) * 0.1]
        }
    }))
};

const mockFleet = {
    type: 'FeatureCollection',
    features: Array.from({ length: 12 }, (_, i) => ({
        type: 'Feature',
        id: i + 100,
        properties: {
            id: `NODE-${200 + i}`,
            type: 'fleet',
            health: 80 + Math.random() * 20,
            load: Math.random() * 100
        },
        geometry: {
            type: 'Point',
            coordinates: [-106.132 + (Math.random() - 0.5) * 0.08, 37.485 + (Math.random() - 0.5) * 0.08]
        }
    }))
};

export const GeospatialIntelligence: React.FC = () => {
    const [viewState, setViewState] = useState({
        longitude: -106.132,
        latitude: 37.485,
        zoom: 13,
        pitch: 45,
        bearing: -17
    });

    const [activeLayers, setActiveLayers] = useState<Set<string>>(new Set(['sensors', 'fleet', 'satellite']));
    const [selectedFeature, setSelectedFeature] = useState<any>(null);
    const [sidebarOpen, setSidebarOpen] = useState(true);

    const toggleLayer = (id: string) => {
        const next = new Set(activeLayers);
        if (next.has(id)) next.delete(id);
        else next.add(id);
        setActiveLayers(next);
    };

    const handleFeatureClick = (evt: any) => {
        const feature = evt.features?.[0];
        if (feature) {
            setSelectedFeature(feature.properties);
            setSidebarOpen(true);
        }
    };

    return (
        <div className="h-full w-full relative flex flex-col bg-[#050308] overflow-hidden">
            {/* Header / HUD Overlay */}
            <div className="absolute top-0 left-0 right-0 z-20 pointer-events-none p-6 flex items-start justify-between">
                <div className="pointer-events-auto bg-black/60 backdrop-blur-xl border border-purple-900/30 p-4 rounded-2xl flex items-center gap-4 shadow-2xl">
                    <div className="bg-blue-600/20 p-2.5 rounded-xl border border-blue-500/20">
                        <Globe className="w-5 h-5 text-blue-400" />
                    </div>
                    <div>
                        <h1 className="text-sm font-black text-white uppercase tracking-tighter">Geospatial Intelligence Center</h1>
                        <p className="text-[9px] text-blue-500 font-mono uppercase tracking-widest mt-0.5">Unified Operational Picture • SLV Basin</p>
                    </div>
                </div>

                <div className="pointer-events-auto flex items-center gap-2 bg-black/60 backdrop-blur-xl border border-purple-900/30 p-2 rounded-xl">
                    <button className="p-2 hover:bg-white/5 rounded-lg transition-all"><Filter className="w-4 h-4 text-slate-400" /></button>
                    <div className="w-px h-6 bg-white/10 mx-1" />
                    <button onClick={() => setSidebarOpen(!sidebarOpen)} className="p-2 hover:bg-white/5 rounded-lg transition-all">
                        <ChevronRight className={`w-4 h-4 text-slate-400 transition-transform ${sidebarOpen ? 'rotate-0' : 'rotate-180'}`} />
                    </button>
                </div>
            </div>

            {/* Main Map Engine */}
            <div className="flex-1 relative">
                <Map
                    {...viewState}
                    onMove={evt => setViewState(evt.viewState)}
                    onClick={handleFeatureClick}
                    interactiveLayerIds={['sensors-layer', 'fleet-layer']}
                    style={{ width: '100%', height: '100%' }}
                    mapStyle="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
                >
                    <NavigationControl position="top-right" />
                    <FullscreenControl position="top-right" />
                    <ScaleControl position="bottom-left" />

                    {/* Sensor Layer */}
                    {activeLayers.has('sensors') && (
                        <Source type="geojson" data={mockSensors}>
                            <Layer
                                id="sensors-layer"
                                type="circle"
                                paint={{
                                    'circle-radius': ['interpolate', ['linear'], ['zoom'], 12, 4, 16, 12],
                                    'circle-color': [
                                        'case',
                                        ['==', ['get', 'status'], 'offline'], '#475569',
                                        ['interpolate', ['linear'], ['get', 'value'], 0.20, '#ef4444', 0.35, '#fbbf24', 0.45, '#10b981']
                                    ],
                                    'circle-opacity': 0.8,
                                    'circle-stroke-width': 2,
                                    'circle-stroke-color': '#000'
                                }}
                            />
                        </Source>
                    )}

                    {/* Fleet Layer */}
                    {activeLayers.has('fleet') && (
                        <Source type="geojson" data={mockFleet}>
                            <Layer
                                id="fleet-layer"
                                type="symbol"
                                layout={{
                                    'icon-image': 'rocket-15',
                                    'icon-size': 1.5,
                                    'text-field': ['get', 'id'],
                                    'text-size': 8,
                                    'text-offset': [0, 1.5],
                                    'text-anchor': 'top'
                                }}
                                paint={{
                                    'text-color': '#fff'
                                }}
                            />
                        </Source>
                    )}
                </Map>

                {/* Layer Control Palette */}
                <div className="absolute bottom-10 left-6 z-20 flex flex-col gap-2">
                    {[
                        { id: 'sensors', label: 'Sensor Matrix', icon: Radio, color: 'text-emerald-400' },
                        { id: 'fleet', label: 'Fleet Assets', icon: Zap, color: 'text-amber-400' },
                        { id: 'satellite', label: 'Satellite Synthesis', icon: Globe, color: 'text-blue-400' },
                        { id: 'ledger', label: 'Water Ledger', icon: ShieldCheck, color: 'text-purple-400' },
                    ].map(layer => (
                        <button
                            key={layer.id}
                            onClick={() => toggleLayer(layer.id)}
                            className={`flex items-center gap-3 px-4 py-3 rounded-2xl border transition-all backdrop-blur-xl ${activeLayers.has(layer.id) ? 'bg-white/10 border-white/20 text-white shadow-lg' : 'bg-black/40 border-purple-900/30 text-slate-500 hover:text-slate-300'}`}
                        >
                            <layer.icon className={`w-4 h-4 ${activeLayers.has(layer.id) ? layer.color : 'text-slate-500'}`} />
                            <span className="text-[10px] font-black uppercase tracking-widest">{layer.label}</span>
                        </button>
                    ))}
                </div>
            </div>

            {/* Diagnostic Sidebar */}
            <div className={`absolute top-24 bottom-6 right-6 w-80 z-20 transition-all duration-500 transform ${sidebarOpen ? 'translate-x-0' : 'translate-x-[calc(100%+24px)]'}`}>
                <div className="h-full bg-black/60 backdrop-blur-xl border border-purple-900/30 rounded-3xl p-6 flex flex-col shadow-2xl relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-4 opacity-5">
                        <MapIcon className="w-32 h-32 text-white" />
                    </div>

                    <div className="flex items-center justify-between mb-8">
                        <h2 className="text-sm font-black text-white uppercase tracking-widest flex items-center gap-2">
                            <Activity className="w-4 h-4 text-blue-400" /> Intelligence Feed
                        </h2>
                        <button onClick={() => setSidebarOpen(false)} className="text-slate-500 hover:text-white"><X className="w-4 h-4" /></button>
                    </div>

                    {selectedFeature ? (
                        <div className="flex-1 space-y-6 animate-in slide-in-from-right duration-300">
                            <div className="bg-white/5 border border-white/5 p-5 rounded-2xl">
                                <p className="text-[9px] font-bold text-blue-400 uppercase tracking-widest mb-1">{selectedFeature.type} Node</p>
                                <p className="text-2xl font-black text-white">{selectedFeature.id}</p>
                                <div className="mt-4 grid grid-cols-2 gap-4">
                                    <div>
                                        <p className="text-[8px] font-bold text-slate-500 uppercase">Health</p>
                                        <p className="text-sm font-mono text-emerald-400">{selectedFeature.health ?? '98.4'}%</p>
                                    </div>
                                    <div>
                                        <p className="text-[8px] font-bold text-slate-500 uppercase">Battery</p>
                                        <p className="text-sm font-mono text-emerald-400">{selectedFeature.battery ?? '72.1'}%</p>
                                    </div>
                                </div>
                            </div>

                            <div className="space-y-4">
                                <h3 className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Diagnostic Logs</h3>
                                {[
                                    { time: '14:22', msg: 'HEARTBEAT_OK', color: 'text-emerald-500' },
                                    { time: '12:05', msg: 'FHE_READY', color: 'text-blue-500' },
                                    { time: '09:15', msg: 'SATELLITE_SYNC_COMPLETE', color: 'text-purple-500' },
                                ].map((log, i) => (
                                    <div key={i} className="flex gap-3 text-[9px] font-mono">
                                        <span className="text-slate-600">{log.time}</span>
                                        <span className={log.color}>{log.msg}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ) : (
                        <div className="flex-1 flex flex-col items-center justify-center text-center p-6 bg-white/5 border border-dashed border-white/10 rounded-2xl">
                            <Info className="w-10 h-10 text-slate-700 mb-4" />
                            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Select an entity on the map to begin diagnostics</p>
                        </div>
                    )}

                    <div className="mt-auto pt-6 border-t border-white/5">
                        <div className="flex items-center justify-between text-[10px] font-bold uppercase tracking-widest mb-3 text-slate-500">
                            <span>Quorum Status</span>
                            <span className="text-emerald-400">ACTIVE</span>
                        </div>
                        <div className="h-1 w-full bg-white/10 rounded-full overflow-hidden">
                            <div className="h-full bg-emerald-500 w-[92%]" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default GeospatialIntelligence;

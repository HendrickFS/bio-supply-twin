import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap, CircleMarker } from 'react-leaflet';
import { Card, Spin, Alert, Button, Select, Space, Tag, Switch } from 'antd';
import { EnvironmentOutlined, ReloadOutlined, LineChartOutlined } from '@ant-design/icons';
import { apiService } from '../../shared/services/api';
import type { TransportBox, TelemetryReading } from '../../shared/services/api';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './BoxTracking.css';

import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

L.Marker.prototype.options.icon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

const parseGeolocation = (geolocation: string) => {
  const coords = geolocation.split(',').map(s => s.trim());
  if (coords.length === 2) {
    const lat = parseFloat(coords[0]);
    const lng = parseFloat(coords[1]);
    if (!isNaN(lat) && !isNaN(lng)) {
      return { lat, lng, name: geolocation };
    }
  }
  return { lat: 42.3601, lng: -71.0589, name: geolocation };
};

const RecenterMap = ({ lat, lng }: { lat: number; lng: number }) => {
  const map = useMap();
  useEffect(() => {
    map.setView([lat, lng], 13);
  }, [lat, lng, map]);
  return null;
};

const getStatusColor = (status: string) => {
  const colors: { [key: string]: string } = {
    'active': 'success',
    'in_transit': 'processing',
    'delivered': 'purple',
    'maintenance': 'warning',
    'inactive': 'error',
  };
  return colors[status.toLowerCase()] || 'default';
};

export const BoxTracking = () => {
  const [boxes, setBoxes] = useState<TransportBox[]>([]);
  const [selectedBoxId, setSelectedBoxId] = useState<string | null>(null);
  const [telemetry, setTelemetry] = useState<TelemetryReading[]>([]);
  const [showRoute, setShowRoute] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchBoxes = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiService.getBoxes();
      setBoxes(data);
      if (data.length > 0 && !selectedBoxId) {
        setSelectedBoxId(data[0].box_id);
      }
    } catch (err) {
      setError('Failed to fetch transport boxes. Please check if the backend is running.');
      console.error('Error fetching boxes:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchTelemetry = async (boxId: string) => {
    try {
      // Fetch all telemetry and filter by box_id matching
      const allTelemetry = await apiService.getTelemetry();
      
      // Find the numeric ID of the selected box
      const selectedBoxData = boxes.find(b => b.box_id === boxId);
      if (selectedBoxData) {
        const boxNumericId = selectedBoxData.id;
        const boxTelemetry = allTelemetry
          .filter(t => t.box === boxNumericId)
          .sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());
        
        setTelemetry(boxTelemetry);
      } else {
        setTelemetry([]);
      }
    } catch (err) {
      console.error('Error fetching telemetry:', err);
      setTelemetry([]);
    }
  };

  useEffect(() => {
    fetchBoxes();
    // Manual refresh only - no auto-reload
  }, []);

  useEffect(() => {
    if (selectedBoxId) {
      fetchTelemetry(selectedBoxId);
    }
  }, [selectedBoxId, boxes]);

  const selectedBox = boxes.find(box => box.box_id === selectedBoxId);
  const selectedLocation = selectedBox 
    ? parseGeolocation(selectedBox.geolocation)
    : null;

  // Parse telemetry locations for route
  const routeCoordinates = telemetry
    .filter(t => t.geolocation && t.geolocation.trim() !== '')
    .map(t => {
      const location = parseGeolocation(t.geolocation);
      return [location.lat, location.lng] as [number, number];
    });

  return (
    <div style={{ padding: '24px' }}>
      <Card 
        title={
          <Space>
            <EnvironmentOutlined />
            <span>Transport Box Location Tracking</span>
          </Space>
        }
        extra={
          <Space>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <LineChartOutlined />
              <span>Show Route</span>
              <Switch checked={showRoute} onChange={setShowRoute} />
            </div>
            <Button 
              icon={<ReloadOutlined />} 
              onClick={() => {
                fetchBoxes();
                if (selectedBoxId) fetchTelemetry(selectedBoxId);
              }}
              loading={loading}
            >
              Refresh
            </Button>
          </Space>
        }
      >
        {error && (
          <Alert
            message="Error"
            description={error}
            type="error"
            closable
            style={{ marginBottom: 16 }}
          />
        )}

        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          {/* Box Selector */}
          <div>
            <label style={{ marginRight: 8, fontWeight: 500 }}>Select Transport Box:</label>
            <Select
              style={{ width: 300 }}
              placeholder="Select a box to track"
              value={selectedBoxId}
              onChange={setSelectedBoxId}
              loading={loading}
              options={boxes.map(box => ({
                label: `${box.box_id} - ${box.geolocation}`,
                value: box.box_id,
              }))}
            />
          </div>

          {selectedBox && (
            <Space style={{ width: '100%', fontSize: 14 }}>
              <span><strong>Box:</strong> {selectedBox.box_id}</span>
              <span><strong>Temp:</strong> {selectedBox.temperature}°C</span>
              <span><strong>Humidity:</strong> {selectedBox.humidity}%</span>
              <Tag color={getStatusColor(selectedBox.status)}>{selectedBox.status}</Tag>
              {telemetry.length > 1 && <span>📍 {telemetry.length} points</span>}
            </Space>
          )}

          {/* Map */}
          {loading ? (
            <div style={{ textAlign: 'center', padding: '100px 0' }}>
              <Spin size="large" tip="Loading map data..." />
            </div>
          ) : selectedLocation ? (
            <div style={{ height: '500px', width: '100%', borderRadius: '8px', overflow: 'hidden' }}>
              <MapContainer
                center={[selectedLocation.lat, selectedLocation.lng]}
                zoom={13}
                style={{ height: '100%', width: '100%' }}
              >
                <TileLayer
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                
                {showRoute && routeCoordinates.length > 1 && (
                  <>
                    <Polyline
                      positions={routeCoordinates}
                      color="#1890ff"
                      weight={3}
                      dashArray="10, 10"
                      interactive={false}
                    />
                    
                    {telemetry.map((reading, index) => {
                      if (!reading.geolocation || reading.geolocation.trim() === '') return null;
                      const location = parseGeolocation(reading.geolocation);
                      const isFirst = index === 0;
                      const isLast = index === telemetry.length - 1;
                      
                      return (
                        <CircleMarker
                          key={`waypoint-${reading.id}`}
                          center={[location.lat, location.lng]}
                          radius={isFirst || isLast ? 6 : 4}
                          fillColor={isFirst ? '#52c41a' : isLast ? '#ff4d4f' : '#1890ff'}
                          color="#fff"
                          weight={2}
                          fillOpacity={0.8}
                          interactive={false}
                          bubblingMouseEvents={false}
                          eventHandlers={{}}
                          pathOptions={{ className: 'no-pointer-events' }}
                        />
                      );
                    })}
                  </>
                )}
                
                {boxes.map(box => {
                  const location = parseGeolocation(box.geolocation);
                  if (showRoute && box.box_id === selectedBoxId && telemetry.length > 0) {
                    return null;
                  }
                  
                  return (
                    <Marker key={box.box_id} position={[location.lat, location.lng]}>
                      <Popup>
                        <div>
                          <h3>Box {box.box_id}</h3>
                          <p><Tag color={getStatusColor(box.status)}>{box.status}</Tag></p>
                          <p>Temp: {box.temperature}°C | Humidity: {box.humidity}%</p>
                          <p>{box.geolocation}</p>
                        </div>
                      </Popup>
                    </Marker>
                  );
                })}
                
                {selectedLocation && (
                  <RecenterMap lat={selectedLocation.lat} lng={selectedLocation.lng} />
                )}
              </MapContainer>
            </div>
          ) : (
            <Alert
              message="No boxes available"
              description="There are no transport boxes to display on the map."
              type="info"
            />
          )}
        </Space>
      </Card>
    </div>
  );
};

/**
 * API Service - Bio Supply Digital Twin
 * 
 * Centralized API calls to backend services
 */

import axios from 'axios';

// Django Core Service - Transport boxes, samples, telemetry
const DJANGO_API_URL = import.meta.env.VITE_DJANGO_API_URL || 'http://localhost:8000';

// FastAPI Digital Twin Service - Stats, health, cache
const FASTAPI_API_URL = import.meta.env.VITE_FASTAPI_API_URL || 'http://localhost:8001';

const djangoApi = axios.create({
  baseURL: DJANGO_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

const fastApi = axios.create({
  baseURL: FASTAPI_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
djangoApi.interceptors.response.use(
  (response: any) => response,
  (error: any) => {
    console.error('Django API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

fastApi.interceptors.response.use(
  (response: any) => response,
  (error: any) => {
    console.error('FastAPI Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export interface Stats {
  num_boxes: number;
  num_samples: number;
  num_active_alerts: number;
  from_cache?: boolean;
}

export interface TransportBox {
  id: number;
  box_id: string;
  geolocation: string;
  temperature: number;
  humidity: number;
  status: string;
  last_updated: string;
}

export interface Sample {
  sample_id: string;
  box: number;
  name: string;
  description: string;
  collected_at: string;
  status: string;
  temperature: number;
  humidity: number;
  last_updated: string;
}

export interface TelemetryReading {
  id: number;
  box: number | null;
  sample: number | null;
  timestamp: string;
  temperature: number;
  humidity: number;
  geolocation: string;
}

export interface CacheStats {
  status: string;
  memory_used?: string;
  total_keys?: number;
}

export interface HealthCheck {
  status: string;
  service: string;
  cache?: CacheStats;
}

// API Methods
export const apiService = {
  // Health & Stats (FastAPI)
  getHealth: async (): Promise<HealthCheck> => {
    const { data } = await fastApi.get('/health');
    return data;
  },

  getStats: async (): Promise<Stats> => {
    const { data } = await fastApi.get('/stats');
    return data;
  },

  getCacheStats: async (): Promise<CacheStats> => {
    const { data } = await fastApi.get('/cache/stats');
    return data;
  },

  clearCache: async (): Promise<void> => {
    await fastApi.delete('/cache/clear');
  },

  // Transport Boxes (Django)
  getBoxes: async (): Promise<TransportBox[]> => {
    const { data } = await djangoApi.get('/api/transport_boxes/');
    return data;
  },

  getBox: async (boxId: string): Promise<TransportBox> => {
    const { data } = await djangoApi.get(`/api/transport_boxes/${boxId}/`);
    return data;
  },

  // Samples (Django)
  getSamples: async (): Promise<Sample[]> => {
    const { data } = await djangoApi.get('/api/samples/');
    return data;
  },

  getSample: async (sampleId: string): Promise<Sample> => {
    const { data } = await djangoApi.get(`/api/samples/${sampleId}/`);
    return data;
  },

  // Telemetry (Django)
  getTelemetry: async (): Promise<TelemetryReading[]> => {
    const { data } = await djangoApi.get('/api/telemetry/');
    return data;
  },

  getBoxTelemetry: async (boxId: number): Promise<TelemetryReading[]> => {
    const { data } = await djangoApi.get(`/api/telemetry/?box=${boxId}`);
    return data;
  },
};

export default djangoApi;

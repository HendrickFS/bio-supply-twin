/**
 * API Service - Bio Supply Digital Twin
 * 
 * Centralized API calls to backend services
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response: any) => response,
  (error: any) => {
    console.error('API Error:', error.response?.data || error.message);
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
  box_id: string;
  geolocation: string;
  temperature: number;
  humidity: number;
  status: string;
  last_updated: string;
}

export interface Sample {
  sample_id: string;
  box_id: number;
  name: string;
  description: string;
  collected_at: string;
  status: string;
  temperature: number;
  humidity: number;
  last_updated: string;
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
  // Health & Stats
  getHealth: async (): Promise<HealthCheck> => {
    const { data } = await api.get('/health');
    return data;
  },

  getStats: async (): Promise<Stats> => {
    const { data } = await api.get('/stats');
    return data;
  },

  getCacheStats: async (): Promise<CacheStats> => {
    const { data } = await api.get('/cache/stats');
    return data;
  },

  clearCache: async (): Promise<void> => {
    await api.delete('/cache/clear');
  },

  // Transport Boxes
  getBoxes: async (): Promise<TransportBox[]> => {
    const { data } = await api.get('/boxes');
    return data;
  },

  getBox: async (boxId: string): Promise<TransportBox> => {
    const { data } = await api.get(`/boxes/${boxId}`);
    return data;
  },

  // Samples
  getSamples: async (): Promise<Sample[]> => {
    const { data } = await api.get('/samples');
    return data;
  },

  getSample: async (sampleId: string): Promise<Sample> => {
    const { data } = await api.get(`/samples/${sampleId}`);
    return data;
  },
};

export default api;

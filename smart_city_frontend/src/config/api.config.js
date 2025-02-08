// src/config/api.config.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const API_ENDPOINTS = {
  dashboard: `${API_BASE_URL}/Dashboard/dashboard`,
  traffic: `${API_BASE_URL}/Traffic/traffic`,
  pollution: `${API_BASE_URL}/Pollution/pollution`,
  waste: `${API_BASE_URL}/Waste/waste`,
  metering: `${API_BASE_URL}/Metering/metering`
};

export default API_BASE_URL;
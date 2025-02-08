const API_BASE_URL = "https://bug-free-happiness-44rgx5vgq5xhjxp7-5000.app.github.dev";


export const API_ENDPOINTS = Object.freeze({
  dashboard: `${API_BASE_URL}/api//Dashboard/dashboard`,
  traffic: `${API_BASE_URL}/api//Traffic/traffic`,
  pollution: `${API_BASE_URL}/api//Pollution/pollution`,
  waste: `${API_BASE_URL}/api//Waste/waste`,
  metering: `${API_BASE_URL}/api//Metering/metering`
});

export { API_BASE_URL };
export default API_ENDPOINTS;

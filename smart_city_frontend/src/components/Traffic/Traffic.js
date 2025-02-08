import React, { useState, useEffect } from "react";
import axios from "axios";
import { API_ENDPOINTS } from "../../config/api.config"; // Import API config
import "./Traffic.css";

const Traffic = () => {
  const [trafficData, setTrafficData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get(API_ENDPOINTS.traffic) // Use API config
      .then((response) => {
        setTrafficData(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Traffic Data Error:", error);
        setError("Error fetching traffic data.");
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="loading">Loading traffic data...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="traffic-container">
      <h2>🚦 Traffic Congestion</h2>
      <table className="traffic-table">
        <thead>
          <tr>
            <th>Location</th>
            <th>Congestion Level (%)</th>
            <th>Average Speed (km/h)</th>
          </tr>
        </thead>
        <tbody>
          {trafficData.map((t) => (
            <tr key={t.id}>
              <td>{t.location}</td>
              <td>{t.congestion_level}%</td>
              <td>{t.average_speed || "N/A"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Traffic;

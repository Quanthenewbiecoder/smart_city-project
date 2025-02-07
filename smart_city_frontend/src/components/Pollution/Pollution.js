import React, { useState, useEffect } from "react";
import axios from "axios";
import './Pollution.css';  // Add your custom styles here

const Pollution = () => {
  const [pollutionData, setPollutionData] = useState([]);
  const [loading, setLoading] = useState(true);  // Loading state
  const [error, setError] = useState(null);  // Error state

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/pollution")
      .then((response) => {
        setPollutionData(response.data);
        setLoading(false);  // Data loaded, set loading to false
      })
      .catch((error) => {
        setError("Error fetching pollution data.");
        setLoading(false);  // Even if there's an error, stop loading
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;  // Show loading message
  }

  if (error) {
    return <div>{error}</div>;  // Show error message
  }

  return (
    <div>
      <h2>🌫 Air Pollution</h2>
      <table className="pollution-table">
        <thead>
          <tr>
            <th>Location</th>
            <th>AQI</th>
          </tr>
        </thead>
        <tbody>
          {pollutionData.map((p) => (
            <tr key={p.id}>
              <td>{p.location}</td>
              <td>{p.air_quality_index}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Pollution;

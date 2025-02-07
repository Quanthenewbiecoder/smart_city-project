import React, { useState, useEffect } from "react";
import axios from "axios";
import './Traffic.css';

const Pollution = () => {
  const [pollutionData, setPollutionData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/pollution`)
      .then((response) => {
        setPollutionData(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Pollution Data Error:", error);
        setError("Error fetching pollution data.");
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

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

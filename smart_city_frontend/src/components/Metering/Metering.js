import React, { useState, useEffect } from "react";
import axios from "axios";
import './Metering.css';

const Metering = () => {
  const [meteringData, setMeteringData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/metering`)
      .then((response) => {
        setMeteringData(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Metering Data Error:", error);
        setError("Error fetching metering data.");
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h2>⚡ Smart Metering</h2>
      <table className="metering-table">
        <thead>
          <tr>
            <th>Location</th>
            <th>Water Usage (L)</th>
            <th>Energy Usage (kWh)</th>
          </tr>
        </thead>
        <tbody>
          {meteringData.map((m) => (
            <tr key={m.id}>
              <td>{m.location}</td>
              <td>{m.water_usage}</td>
              <td>{m.energy_usage}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Metering;

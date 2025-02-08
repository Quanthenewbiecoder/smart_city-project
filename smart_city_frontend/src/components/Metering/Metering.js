import React from "react";
import './Metering.css';

const Metering = ({ data }) => {
  if (!data) return <div>Loading...</div>;
  if (data.length === 0) return <div>No metering data available.</div>;

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
          {data.map((m) => (
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

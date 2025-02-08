import React from "react";
import './Pollution.css';

const Pollution = ({ data }) => {
  if (!data) return <div>Loading...</div>;
  if (data.length === 0) return <div>No pollution data available.</div>;

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
          {data.map((p) => (
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

import React, { useState, useEffect } from "react";
import axios from "axios";
import './Waste.css';

const Waste = () => {
  const [wasteData, setWasteData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/waste`)
      .then((response) => {
        setWasteData(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Waste Data Error:", error);
        setError("Error fetching waste data.");
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h2>🗑 Waste Management</h2>
      <table className="waste-table">
        <thead>
          <tr>
            <th>Location</th>
            <th>Bin Fill Level</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {wasteData.map((w) => (
            <tr key={w.id}>
              <td>{w.location}</td>
              <td>{w.bin_fill_level}%</td>
              <td>
                {w.bin_fill_level >= 80 ? (
                  <span className="status-full">Full</span>
                ) : (
                  <span className="status-ok">OK</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Waste;

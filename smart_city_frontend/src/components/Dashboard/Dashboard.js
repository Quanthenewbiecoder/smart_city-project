import React, { useState, useEffect } from "react";
import axios from "axios";
import { API_ENDPOINTS } from "../../config/api.config"; // Import API config
import "./Dashboard.css";

import Traffic from "../Traffic/Traffic";
// import Metering from "../Metering/Metering";
// import Pollution from "../Pollution/Pollution";
// import Waste from "../Waste/Waste";

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedSection, setSelectedSection] = useState("traffic"); // Default section

  useEffect(() => {
    axios
      .get(API_ENDPOINTS.dashboard) // Use API config
      .then((response) => {
        setDashboardData(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching dashboard data:", error);
        setError("Error loading dashboard data.");
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="loading">📊 Loading Smart City Dashboard...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="dashboard-container">
      <h2>📊 Smart City Dashboard</h2>

      {/* Navigation Buttons */}
      <div className="dashboard-nav">
        <button onClick={() => setSelectedSection("traffic")}>🚦 Traffic Congestion</button>
        {/*<button onClick={() => setSelectedSection("pollution")}>🌫️ Air Pollution</button>
        <button onClick={() => setSelectedSection("waste")}>♻️ Waste Management</button>
        <button onClick={() => setSelectedSection("metering")}>🔌 Smart Metering</button>*/}
      </div>

      {/* Section Rendering */}
      {selectedSection === "traffic" && <Traffic data={dashboardData?.traffic || []} />}
      {/*{selectedSection === "pollution" && <Pollution data={dashboardData?.pollution || []} />}
      {selectedSection === "waste" && <Waste data={dashboardData?.waste || []} />}
      {selectedSection === "metering" && <Metering data={dashboardData?.metering || []} />}*/}
    </div>
  );
};

export default Dashboard;

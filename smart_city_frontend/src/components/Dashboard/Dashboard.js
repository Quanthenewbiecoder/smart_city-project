import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Dashboard.css";

import Metering from "../Metering/Metering";
import Pollution from "../Pollution/Pollution";
import Waste from "../Waste/Waste";
import Traffic from "../Traffic/Traffic"; // Added import

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [selectedSection, setSelectedSection] = useState("traffic"); // Default section

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/dashboard")
      .then((response) => setDashboardData(response.data))
      .catch((error) => console.error("Error fetching dashboard data:", error));
  }, []);

  return (
    <div>
      <h2>📊 Smart City Dashboard</h2>

      {/* Section Buttons */}
      <div className="dashboard-nav">
        <button className="dashboard-btn" onClick={() => setSelectedSection("traffic")}>Traffic Congestion</button>
        <button className="dashboard-btn" onClick={() => setSelectedSection("pollution")}>Air Pollution</button>
        <button className="dashboard-btn" onClick={() => setSelectedSection("waste")}>Waste Management</button>
        <button className="dashboard-btn" onClick={() => setSelectedSection("metering")}>Smart Metering</button>
      </div>

      {/* Display the selected section */}
      {selectedSection === "traffic" && dashboardData && <Traffic data={dashboardData.traffic} />}
      {selectedSection === "pollution" && dashboardData && <Pollution data={dashboardData.pollution} />}
      {selectedSection === "waste" && dashboardData && <Waste data={dashboardData.waste} />}
      {selectedSection === "metering" && dashboardData && <Metering data={dashboardData.metering} />}
    </div>
  );
};

export default Dashboard;

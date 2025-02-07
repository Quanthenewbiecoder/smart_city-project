import React from "react";
import Traffic from "./components/Traffic/Traffic";
import Pollution from "./components/Pollution/Pollution";
import Waste from "./components/Waste/Waste";
import Metering from "./components/Metering/Metering";
import Dashboard from "./components/Dashboard/Dashboard";

const App = () => {
  return (
    <div>
      <h1>🏙 Smart City Management</h1>
      <Dashboard />
      <Traffic />
      <Pollution />
      <Waste />
      <Metering />
    </div>
  );
};

export default App;

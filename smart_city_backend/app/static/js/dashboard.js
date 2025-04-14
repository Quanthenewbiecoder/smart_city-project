document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/dashboard")
      .then(res => res.json())
      .then(data => {
        const categories = ["traffic", "pollution", "waste", "metering"];
  
        categories.forEach(category => {
          const container = document.getElementById(`${category}-cards`);
          
          // Display data in cards as before
          if (data[category]) {
            data[category].forEach(entry => {
              const card = document.createElement("div");
              card.className = "card";
              card.innerHTML = `
                <h3>${category.toUpperCase()}</h3>
                <p><strong>Location:</strong> ${entry.location}</p>
                ${Object.entries(entry)
                  .filter(([k]) => k !== "location")
                  .map(([k, v]) => `<p><strong>${k}:</strong> ${v}</p>`)
                  .join("")}
              `;
              container.appendChild(card);
            });
          }
  
          // If it's the 'metering' category, render a chart
          if (category === 'metering' && data[category].length > 0) {
            const meteringData = data[category][0]; // Assuming only one metering entry in the list
            const prediction = meteringData.prediction;
  
            const chartContainer = document.createElement("div");
            chartContainer.className = "card";
            chartContainer.innerHTML = `
              <h3>${category.toUpperCase()} Prediction</h3>
              <canvas id="metering-chart"></canvas>
            `;
            container.appendChild(chartContainer);
  
            // Extract the periods and predicted values for the chart
            const periods = prediction.map(p => p.period);
            const predictedUsage = prediction.map(p => p.predicted_water_usage);
  
            // Render the chart using Chart.js
            const ctx = document.getElementById('metering-chart').getContext('2d');
            const chart = new Chart(ctx, {
              type: 'line', // You can change this to 'bar' if you prefer a bar chart
              data: {
                labels: periods, // X-axis values (periods)
                datasets: [{
                  label: 'Predicted Water Usage',
                  data: predictedUsage, // Y-axis values (predicted water usage)
                  fill: false,
                  borderColor: 'rgb(75, 192, 192)',
                  tension: 0.1
                }]
              },
              options: {
                responsive: true,
                scales: {
                  x: {
                    title: {
                      display: true,
                      text: 'Period'
                    }
                  },
                  y: {
                    title: {
                      display: true,
                      text: 'Predicted Water Usage (L)'
                    }
                  }
                }
              }
            });
          }
        });
      })
      .catch(err => console.error("Error fetching dashboard data:", err));
  });
  
document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/home/data")
      .then(res => res.json())
      .then(data => {
        const latestContainer = document.getElementById("latest-data");
        const predictionsContainer = document.getElementById("predicted-data");
  
        const latest = data.latest_data;
        const predicted = data.predictions;
  
        for (let key in latest) {
          latest[key].forEach(entry => {
            const card = document.createElement("div");
            card.className = "card";
            card.innerHTML = `
              <h3>${key.toUpperCase()}</h3>
              <p><strong>Location:</strong> ${entry.location}</p>
              ${Object.entries(entry).filter(([k]) => k !== "location").map(([k, v]) => `<p><strong>${k}:</strong> ${v}</p>`).join('')}
            `;
            latestContainer.appendChild(card);
          });
        }
  
        for (let key in predicted) {
          const prediction = predicted[key];
          const card = document.createElement("div");
          card.className = "card";
          card.innerHTML = `
            <h3>${key.toUpperCase()} Prediction</h3>
            <pre>${JSON.stringify(prediction, null, 2)}</pre>
          `;
          predictionsContainer.appendChild(card);
        }
      });
  });
  
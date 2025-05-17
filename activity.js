// Activity Logs Page

function initializeActivity() { fetchLogs(); }

function fetchLogs() {
   fetch("/api/logs")
      .then(res => res.json())
      .then(data => renderLogs(data.logs))
      .catch(err => console.error("Error fetching logs:", err));
}

function renderLogs(logs) {
   const logsContainer = document.getElementById("activity-logs");
   logsContainer.innerHTML = "";

   logs.forEach(log => logsContainer.innerHTML += `
       <div>
           <p>${log.timestamp} - ${log.actionType}</p>
       </div>`);
}

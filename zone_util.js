// Zone Utilization Page

function initializeZoneUtil() { loadZoneUtilization(); }

function loadZoneUtilization() {
   fetch("/api/zone-utilization")
      .then(res => res.json())
      .then(data => renderZones(data.zones))
      .catch(err => console.error("Error loading zones:", err));
}

function renderZones(zones) {
   const zoneContainer = document.getElementById("zones");

   zones.forEach(zone => zoneContainer.innerHTML += `
       <div>
           <h4>${zone.name}</h4>
           <p>Utilization: ${zone.utilization}%</p>
       </div>`);
}

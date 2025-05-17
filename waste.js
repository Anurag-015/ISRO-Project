// Waste Management Page

function initializeWaste() { identifyWaste(); }

// Identify waste items via API call
function identifyWaste() {
   fetch("/api/waste/identify")
      .then(res => res.json())
      .then(data => renderWasteItems(data.wasteItems))
      .catch(err => console.error("Error identifying waste:", err));
}

function renderWasteItems(wasteItems) {
   const wasteContainer = document.getElementById("waste-items");
   wasteContainer.innerHTML = "";

   wasteItems.forEach(item => wasteContainer.innerHTML += `
       <div>
           <h4>${item.name}</h4>
           <p>Reason: ${item.reason}</p>
       </div>`);
}

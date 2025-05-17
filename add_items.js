// Add Items Page

function initializeAddItems() { setupAddItemForm(); }

function setupAddItemForm() {
   const form = document.getElementById("add-item-form");

   form.addEventListener("submit", e => {
      e.preventDefault();

      const formData = new FormData(form);
      const itemData = Object.fromEntries(formData.entries());

      addItem(itemData);
   });
}

function addItem(itemData) {
   fetch("/api/items", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(itemData)
   }).then(res => res.json())
     .then(() => alert("Item added successfully!"))
     .catch(err => console.error("Error adding item:", err));
}

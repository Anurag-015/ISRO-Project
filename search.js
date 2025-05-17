// JavaScript for the Search and Retrieve page

// Initialize search functionality
function initializeSearch() {
    const searchForm = document.getElementById('search-form');

    if (searchForm) {
        searchForm.addEventListener('submit', e => { e.preventDefault(); performSearch(); });
    }
}

// Perform search using API
function performSearch() {
    const searchInput = document.getElementById('search-input');

    if (!searchInput.value.trim()) return alert("Please enter a search term.");

    fetch(`/api/search?itemName=${encodeURIComponent(searchInput.value.trim())}`)
        .then(response => response.json())
        .then(data => renderSearchResults(data))
        .catch(error => console.error("Error performing search:", error));
}

// Render search results to the DOM
function renderSearchResults(data) {
   const resultsContainer = document.getElementById("search-results");
   resultsContainer.innerHTML = ""; // Clear previous results

   if (!data.found || !data.item) return resultsContainer.innerHTML = "<p>No results found.</p>";

   const itemCard = `
       <div>
           <h3>${data.item.name}</h3>
           <p>Item ID: ${data.item.itemId}</p>
           <p>Container ID: ${data.item.containerId}</p>
       </div>`;
   resultsContainer.innerHTML += itemCard;
}

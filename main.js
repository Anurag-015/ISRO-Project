// Main JavaScript file for the Cargo Stowage Management System

// Global state
let currentDate = "2025-04-06";
let containers = [];
let items = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    // Check if we're on the main dashboard page
    if (document.querySelector('.dashboard')) {
        initializeDashboard();
    }

    // Check page type and initialize specific functionality
    if (document.querySelector('.search-page')) {
        initializeSearch();
    } else if (document.querySelector('.waste-page')) {
        initializeWaste();
    } else if (document.querySelector('.activity-page')) {
        initializeActivity();
    } else if (document.querySelector('.add-items-page')) {
        initializeAddItems();
    } else if (document.querySelector('.zone-util-page')) {
        initializeZoneUtil();
    }

    // Setup navigation links
    setupNavigation();
});

// Setup navigation links and active page styling
function setupNavigation() {
    const currentPage = window.location.pathname.split('/').pop();

    // Add active class to current page in navigation
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href').split('/').pop();
        if (linkPath === currentPage || (currentPage === '' && linkPath === 'index.html')) {
            link.classList.add('active');
        }
    });
}

// Initialize dashboard with stats and data
function initializeDashboard() {
    // Get dashboard statistics
    fetchDashboardStats();

    // Get current date
    fetchCurrentDate();

    // Setup time simulation buttons
    setupTimeSimulation();
}

// Fetch current system date
function fetchCurrentDate() {
    document.getElementById('current-date').textContent = currentDate;
}

// Setup time simulation buttons
function setupTimeSimulation() {
    const nextDayBtn = document.getElementById('next-day-btn');
    const fastForwardBtn = document.getElementById('fast-forward-btn');

    if (nextDayBtn) {
        nextDayBtn.addEventListener('click', () => {
            simulateNextDay();
        });
    }

    if (fastForwardBtn) {
        fastForwardBtn.addEventListener('click', () => {
            const days = prompt('How many days?', '7');
            if (days && !isNaN(days) && parseInt(days) > 0) {
                simulateDays(parseInt(days));
            }
        });
    }
}

// Simulate next day
function simulateNextDay() {
    fetch('/api/simulate/day', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ itemsUsed: [] })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                currentDate = data.newDate;
                fetchCurrentDate();
                fetchDashboardStats();
                showNotification(`Date advanced to ${currentDate}`);
                if (data.changes.newlyExpired && data.changes.newlyExpired.length > 0) {
                    showAlert(`${data.changes.newlyExpired.length} items have expired!`);
                }
            }
        })
        .catch(error => console.error('Error simulating next day:', error));
}

// Simulate multiple days
function simulateDays(days) {
    fetch('/api/simulate/days', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ days, itemsUsedDaily: [] })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                currentDate = data.newDate;
                fetchCurrentDate();
                fetchDashboardStats();
                showNotification(`Date advanced by ${days} days to ${currentDate}`);
                if (data.changes.newlyExpired && data.changes.newlyExpired.length > 0) {
                    showAlert(`${data.changes.newlyExpired.length} items have expired!`);
                }
            }
        })
        .catch(error => console.error('Error simulating days:', error));
}

// Fetch dashboard statistics
function fetchDashboardStats() {
    fetch('/api/search?itemName=all')
        .then(response => response.json())
        .then(data => document.getElementById('total-items').textContent = data.items?.length || 0)
        .catch(error => console.error('Error fetching items:', error));

    fetch('/api/waste/identify')
        .then(response => response.json())
        .then(data => document.getElementById('waste-items').textContent = data.wasteItems?.length || 0)
        .catch(error => console.error('Error fetching waste items:', error));
}

// Show notification
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => notification.classList.add('show'), 100);

    setTimeout(() => notification.classList.remove('show'), 3000);
}

// Show alert
function showAlert(message) { alert(message); }

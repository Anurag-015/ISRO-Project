document.addEventListener('DOMContentLoaded', () => {
    // Initialize the system date display
    updateSystemDate();

    // Fetch and display dashboard statistics
    fetchDashboardStats();

    // Set up time simulation buttons
    setupTimeSimulationButtons();

    // Set up navigation event handlers
    setupNavigation();
});

function updateSystemDate() {
    const dateElement = document.getElementById('current-date');
    if (dateElement) {
        // Fetch current system date from API
        fetch('/api/simulate/day', { method: 'GET' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    dateElement.textContent = new Date(data.currentDate).toLocaleDateString('en-US', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                    });
                }
            })
            .catch(error => console.error('Error fetching system date:', error));
    }
}

function fetchDashboardStats() {
    // Update total items count
    fetch('/api/search?itemName=all')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const totalItemsElement = document.getElementById('total-items');
                if (totalItemsElement) {
                    totalItemsElement.textContent = data.items ? data.items.length : 0;
                }
            }
        })
        .catch(error => console.error('Error fetching total items:', error));

    // Update expired items count
    fetch('/api/waste/identify')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const expiredItemsElement = document.getElementById('expired-items');
                if (expiredItemsElement) {
                    expiredItemsElement.textContent = data.wasteItems ? data.wasteItems.length : 0;
                }
            }
        })
        .catch(error => console.error('Error fetching waste items:', error));
}

function setupTimeSimulationButtons() {
    const nextDayButton = document.getElementById('next-day-btn');
    const fastForwardButton = document.getElementById('fast-forward-btn');

    if (nextDayButton) {
        nextDayButton.addEventListener('click', () => {
            simulateNextDay();
        });
    }

    if (fastForwardButton) {
        fastForwardButton.addEventListener('click', () => {
            const days = prompt('Enter number of days to simulate:', '7');
            if (days && !isNaN(days) && parseInt(days) > 0) {
                simulateDays(parseInt(days));
            }
        });
    }
}

function simulateNextDay() {
    fetch('/api/simulate/day', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ itemsUsed: [] })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateSystemDate();
                fetchDashboardStats();
                showNotification(`Advanced to ${data.newDate}`);

                // Show alerts for newly expired items
                if (data.changes && data.changes.newlyExpired && data.changes.newlyExpired.length > 0) {
                    showAlert(`${data.changes.newlyExpired.length} items have expired!`);
                }
            }
        })
        .catch(error => console.error('Error simulating next day:', error));
}

function simulateDays(days) {
    fetch('/api/simulate/days', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            days: days,
            itemsUsedDaily: []
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateSystemDate();
                fetchDashboardStats();
                showNotification(`Advanced ${days} days to ${data.newDate}`);

                // Show alerts for newly expired items
                if (data.changes && data.changes.newlyExpired && data.changes.newlyExpired.length > 0) {
                    showAlert(`${data.changes.newlyExpired.length} items have expired!`);
                }
            }
        })
        .catch(error => console.error('Error simulating multiple days:', error));
}

function setupNavigation() {
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            // Update active link styling
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('show');
    }, 100);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function showAlert(message) {
    alert(message);
}

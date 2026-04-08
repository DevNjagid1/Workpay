// API Configuration
// Empty string means all endpoints are relative to the current origin
const API_BASE = '';

// Helper function for API calls
async function apiCall(endpoint, options = {}) {
    const url = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;

    const config = {
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
            ...options.headers
        },
        ...options
    };

    try {
        const response = await fetch(url, config);
        if (!response.ok) {
            let errorMsg = `HTTP error! status: ${response.status}`;
            try {
                const errData = await response.json();
                if (errData.message) errorMsg = errData.message;
            } catch (_) {}
            throw new Error(errorMsg);
        }
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Show notification messages
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 5px;
        color: white;
        font-weight: 500;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        max-width: 300px;
        word-wrap: break-word;
    `;

    switch (type) {
        case 'success':  notification.style.backgroundColor = '#10b981'; break;
        case 'error':    notification.style.backgroundColor = '#ef4444'; break;
        case 'warning':  notification.style.backgroundColor = '#f59e0b'; break;
        default:         notification.style.backgroundColor = '#3b82f6';
    }

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            if (notification.parentNode) notification.parentNode.removeChild(notification);
        }, 300);
    }, 5000);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-KE', {
        style: 'currency', currency: 'KES', minimumFractionDigits: 0
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-KE', {
        year: 'numeric', month: 'short', day: 'numeric'
    });
}

function formatDateTime(dateTimeString) {
    return new Date(dateTimeString).toLocaleString('en-KE', {
        year: 'numeric', month: 'short', day: 'numeric',
        hour: '2-digit', minute: '2-digit'
    });
}

// CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to   { transform: translateX(0);    opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0);    opacity: 1; }
        to   { transform: translateX(100%); opacity: 0; }
    }
    .notification-success { box-shadow: 0 4px 6px rgba(16, 185, 129, 0.1); }
    .notification-error   { box-shadow: 0 4px 6px rgba(239, 68, 68,  0.1); }
    .notification-warning { box-shadow: 0 4px 6px rgba(245, 158, 11, 0.1); }
    .notification-info    { box-shadow: 0 4px 6px rgba(59,  130, 246, 0.1); }
`;
document.head.appendChild(style);

// Export for use in other files
window.API = {
    call:             apiCall,
    showNotification: showNotification,
    formatCurrency:   formatCurrency,
    formatDate:       formatDate,
    formatDateTime:   formatDateTime
};
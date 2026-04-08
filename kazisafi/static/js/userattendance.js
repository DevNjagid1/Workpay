// User Attendance JavaScript - Simplified for Django template
document.addEventListener('DOMContentLoaded', function () {
    updateClock();
    setInterval(updateClock, 1000);
    console.log('User attendance page loaded');
});

// Update current time display
function updateClock() {
    const now = new Date();
    const timeEl = document.getElementById('currentTime');
    const dateEl = document.getElementById('currentDate');
    if (timeEl) timeEl.textContent = now.toLocaleTimeString('en-KE', {
        hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
    });
    if (dateEl) dateEl.textContent = now.toLocaleDateString('en-KE', {
        weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
    });
}

// Mark attendance - simplified
async function markAttendance() {
    console.log('markAttendance function called');
    const markBtn = document.querySelector('.mark-btn');
    if (!markBtn) return;
    
    const originalText = markBtn.textContent;
    markBtn.disabled = true;
    markBtn.textContent = 'Marking...';

    try {
        const response = await window.API.call('/api/mark-attendance/', {
            method: 'POST',
            body: JSON.stringify({})
        });

        if (response.status === 'success') {
            window.API.showNotification('Attendance marked successfully!', 'success');
            setTimeout(() => window.location.reload(), 2000);
        } else {
            window.API.showNotification(response.message || 'Failed to mark attendance', 'error');
            markBtn.disabled = false;
            markBtn.textContent = originalText;
        }
    } catch (error) {
        console.error('Attendance error:', error);
        window.API.showNotification('Error marking attendance. Please try again.', 'error');
        markBtn.disabled = false;
        markBtn.textContent = originalText;
    }
}
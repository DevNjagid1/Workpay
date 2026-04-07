// User Attendance JavaScript - Dynamic Backend Integration
document.addEventListener('DOMContentLoaded', function() {
    updateClock();
    setInterval(updateClock, 1000);
    loadAttendanceHistory();
    
    // Mark attendance button
    const markBtn = document.querySelector('.mark-btn');
    if (markBtn) {
        markBtn.addEventListener('click', markAttendance);
    }
});

// Update current time
function updateClock() {
    const now = new Date();
    const timeOptions = { 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit',
        hour12: false 
    };
    const dateOptions = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    
    const timeString = now.toLocaleTimeString('en-KE', timeOptions);
    const dateString = now.toLocaleDateString('en-KE', dateOptions);
    
    const timeElement = document.getElementById('currentTime');
    const dateElement = document.getElementById('currentDate');
    
    if (timeElement) timeElement.textContent = timeString;
    if (dateElement) dateElement.textContent = dateString;
}

// Mark attendance via API
async function markAttendance() {
    console.log('markAttendance function called');
    const markBtn = document.querySelector('.mark-btn');
    if (markBtn) {
        markBtn.disabled = true;
        markBtn.textContent = 'Marking...';
    }
    
    try {
        console.log('Making API call to /api/mark-attendance/');
        const response = await API.call('/api/mark-attendance/', {
            method: 'POST'
        });
        
        console.log('API response:', response);
        
        if (response.status === 'success') {
            API.showNotification('Attendance marked successfully!', 'success');
            loadAttendanceHistory();
            updateAttendanceStatus();
        } else {
            API.showNotification(response.message || 'Failed to mark attendance', 'error');
        }
    } catch (error) {
        console.error('Attendance error:', error);
        API.showNotification('Error marking attendance', 'error');
    } finally {
        if (markBtn) {
            markBtn.disabled = false;
            markBtn.textContent = 'Mark Attendance for Today';
        }
    }
}

// Load attendance history from API
async function loadAttendanceHistory() {
    try {
        const response = await API.call('/api/user-attendance-history/');
        if (response.status === 'success') {
            updateAttendanceTable(response.data);
            updateSummaryStats(response.data);
        }
    } catch (error) {
        console.error('Error loading attendance history:', error);
        // Fallback to template-rendered data if API fails
        updateSummaryStatsFromTemplate();
    }
}

// Update attendance table with dynamic data
function updateAttendanceTable(attendances) {
    const tbody = document.getElementById('historyBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    if (attendances.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="4" style="text-align: center; padding: 2rem;">
                    No attendance history found.
                </td>
            </tr>
        `;
        return;
    }
    
    attendances.forEach(attendance => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${API.formatDate(attendance.date)}</td>
            <td>${new Date(attendance.date).toLocaleDateString('en-KE', { weekday: 'long' })}</td>
            <td>${attendance.check_in ? new Date(attendance.check_in).toLocaleTimeString('en-KE', { hour: '2-digit', minute: '2-digit' }) : '--'}</td>
            <td>
                <span class="status-badge ${attendance.status}">
                    ${attendance.status.charAt(0).toUpperCase() + attendance.status.slice(1)}
                </span>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Update summary statistics
function updateSummaryStats(attendances) {
    const pendingCount = attendances.filter(a => a.status === 'pending').length;
    const approvedCount = attendances.filter(a => a.status === 'approved').length;
    const rejectedCount = attendances.filter(a => a.status === 'rejected').length;
    
    const pendingElement = document.getElementById('countPending');
    const approvedElement = document.getElementById('countApproved');
    const rejectedElement = document.getElementById('countRejected');
    
    if (pendingElement) pendingElement.textContent = pendingCount;
    if (approvedElement) approvedElement.textContent = approvedCount;
    if (rejectedElement) rejectedElement.textContent = rejectedCount;
}

// Fallback: Update stats from template-rendered data
function updateSummaryStatsFromTemplate() {
    const pendingElement = document.getElementById('countPending');
    const approvedElement = document.getElementById('countApproved');
    const rejectedElement = document.getElementById('countRejected');
    
    // Get values from template if available
    if (pendingElement && pendingElement.textContent.trim() !== '') {
        // Values already rendered by Django template
        return;
    }
}

// Update attendance status after marking
function updateAttendanceStatus() {
    setTimeout(() => {
        window.location.reload();
    }, 2000);
}

// Filter attendance by status
function filterAttendance(status) {
    const rows = document.querySelectorAll('#historyBody tr');
    rows.forEach(row => {
        const statusBadge = row.querySelector('.status-badge');
        if (statusBadge) {
            const rowStatus = statusBadge.textContent.toLowerCase();
            if (status === 'all' || rowStatus === status) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        }
    });
}

// Export attendance data
function exportAttendance() {
    const rows = document.querySelectorAll('#historyBody tr');
    let csv = 'Date,Day,Check-in Time,Status\n';
    
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        const rowData = Array.from(cells).map(cell => `"${cell.textContent}"`).join(',');
        csv += rowData + '\n';
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `attendance_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Real-time updates (optional - WebSocket or polling)
function startRealTimeUpdates() {
    setInterval(async () => {
        try {
            const response = await API.call('/api/attendance-updates/');
            if (response.status === 'success' && response.has_updates) {
                loadAttendanceHistory();
            }
        } catch (error) {
            console.log('Real-time updates not available');
        }
    }, 30000); // Check every 30 seconds
}

// Initialize real-time updates
document.addEventListener('DOMContentLoaded', function() {
    // Uncomment to enable real-time updates
    // startRealTimeUpdates();
});
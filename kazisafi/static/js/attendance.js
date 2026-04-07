// Remove hardcoded employees - data will come from Django template

function calculateOvertime(checkInStr, checkOutStr) {
    const [inH, inM] = checkInStr.split(':').map(Number);
    const [outH, outM] = checkOutStr.split(':').map(Number);
    const eightAmMinutes = 8 * 60;
    const fourPmMinutes = 16 * 60;
    const checkInTotalMinutes = inH * 60 + inM;
    const checkOutTotalMinutes = outH * 60 + outM;

    const lateness = Math.max(0, checkInTotalMinutes - eightAmMinutes);
    const potentialOT = Math.max(0, checkOutTotalMinutes - fourPmMinutes);
    const netOT = Math.max(0, potentialOT - lateness);
    
    return (netOT / 60).toFixed(1);
}

function updateStatus(id, newStatus) {
    // This will be handled by Django view, not JavaScript
    console.log(`Update status for ${id} to ${newStatus}`);
}

async function approveAttendance(id) {
    try {
        const response = await API.call('/api/approve-attendance/', {
            method: 'POST',
            body: JSON.stringify({ attendance_id: id })
        });
        
        if (response.status === 'success') {
            API.showNotification('Attendance approved successfully!', 'success');
            updatePendingBanner(getCurrentAttendanceData());
            updateAttendanceRow(id, 'approved', response.data);
        } else {
            API.showNotification(response.message || 'Failed to approve attendance', 'error');
        }
    } catch (error) {
        API.showNotification('Error approving attendance', 'error');
        console.error('Approval error:', error);
    }
}

async function rejectAttendance(id) {
    try {
        const response = await API.call('/api/reject-attendance/', {
            method: 'POST',
            body: JSON.stringify({ attendance_id: id })
        });
        
        if (response.status === 'success') {
            API.showNotification('Attendance rejected successfully!', 'success');
            updatePendingBanner(getCurrentAttendanceData());
            updateAttendanceRow(id, 'rejected');
        } else {
            API.showNotification(response.message || 'Failed to reject attendance', 'error');
        }
    } catch (error) {
        API.showNotification('Error rejecting attendance', 'error');
        console.error('Rejection error:', error);
    }
}

function updateAttendanceRow(id, status, data) {
    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (row) {
        const statusCell = row.querySelector('.status-pill');
        const actionCell = row.querySelector('.action-cell');
        
        if (statusCell) {
            statusCell.className = `status-pill ${status}`;
            statusCell.textContent = status.charAt(0).toUpperCase() + status.slice(1);
        }
        
        if (actionCell && data) {
            actionCell.innerHTML = `
                <div class="earnings-details">
                    <small>Work: ${data.work_hours}h | Regular: ${data.regular_hours}h | OT: ${data.overtime_hours}h</small><br>
                    <small>Pay: KES ${data.total_pay} (Regular: KES ${data.regular_pay} + OT: KES ${data.overtime_pay})</small>
                </div>
            `;
        }
    }
}

function getCurrentAttendanceData() {
    // Get current attendance data from the table
    const rows = document.querySelectorAll('#attendanceBody tr');
    return Array.from(rows).map(row => ({
        id: row.dataset.id,
        status: row.dataset.status
    }));
}

function updatePendingBanner(data) {
    const pendingCount = data.filter(r => r.status === 'pending').length;
    const banner = document.getElementById('adminAlert');
    const text = document.getElementById('pendingCountText');
    
    if (pendingCount > 0) {
        banner.style.display = 'flex';
        text.innerText = `${pendingCount} pending attendance records`;
    } else {
        banner.style.display = 'none';
    }
}

function renderTable() {
    // Table is rendered by Django template, no JavaScript rendering needed
    console.log('Table rendered by Django template');
}

function viewDetails(id) {
    // Show attendance details modal or redirect to details page
    console.log(`View details for attendance ID: ${id}`);
    // For now, just show a simple alert
    alert(`Viewing details for attendance record ${id}`);
}

function manageActiveLink() {
    const currentPath = window.location.pathname.split("/").pop();
    const navLinks = document.querySelectorAll('.nav-item');

    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        
        if (currentPath === linkPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    renderTable();
    manageActiveLink();
});

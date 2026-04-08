// attendance.js — Admin attendance management
// Requires api.js to be loaded first (window.API must exist)

function calculateOvertime(checkInStr, checkOutStr) {
    const [inH,  inM]  = checkInStr.split(':').map(Number);
    const [outH, outM] = checkOutStr.split(':').map(Number);
    const eightAm = 8 * 60, fourPm = 16 * 60;
    const checkIn  = inH  * 60 + inM;
    const checkOut = outH * 60 + outM;
    const lateness   = Math.max(0, checkIn  - eightAm);
    const potentialOT = Math.max(0, checkOut - fourPm);
    return ((Math.max(0, potentialOT - lateness)) / 60).toFixed(1);
}

// ── Approve ───────────────────────────────────────────────────────────────────
async function approveAttendance(id) {
    const btn = document.querySelector(`tr[data-id="${id}"] .approve-btn`);
    if (btn) { btn.disabled = true; btn.textContent = 'Approving…'; }

    try {
        const response = await window.API.call('/api/approve-attendance/', {
            method: 'POST',
            body: JSON.stringify({ attendance_id: id })   // ✅ JSON body
        });

        if (response.status === 'success') {
            window.API.showNotification('Attendance approved successfully!', 'success');
            updateAttendanceRow(id, 'approved', response.data);
            refreshPendingBanner();
        } else {
            window.API.showNotification(response.message || 'Failed to approve attendance', 'error');
            if (btn) { btn.disabled = false; btn.textContent = 'Approve'; }
        }
    } catch (error) {
        window.API.showNotification('Error approving attendance', 'error');
        console.error('Approval error:', error);
        if (btn) { btn.disabled = false; btn.textContent = 'Approve'; }
    }
}

// ── Reject ────────────────────────────────────────────────────────────────────
async function rejectAttendance(id) {
    if (!confirm('Are you sure you want to reject this attendance record?')) return;

    const btn = document.querySelector(`tr[data-id="${id}"] .reject-btn`);
    if (btn) { btn.disabled = true; btn.textContent = 'Rejecting…'; }

    try {
        const response = await window.API.call('/api/reject-attendance/', {
            method: 'POST',
            body: JSON.stringify({ attendance_id: id })   // ✅ JSON body
        });

        if (response.status === 'success') {
            window.API.showNotification('Attendance rejected successfully!', 'success');
            updateAttendanceRow(id, 'rejected', null);
            refreshPendingBanner();
        } else {
            window.API.showNotification(response.message || 'Failed to reject attendance', 'error');
            if (btn) { btn.disabled = false; btn.textContent = 'Reject'; }
        }
    } catch (error) {
        window.API.showNotification('Error rejecting attendance', 'error');
        console.error('Rejection error:', error);
        if (btn) { btn.disabled = false; btn.textContent = 'Reject'; }
    }
}

// ── DOM helpers ───────────────────────────────────────────────────────────────
function updateAttendanceRow(id, status, data) {
    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (!row) return;

    // Update status pill
    const pill = row.querySelector('.status-pill');
    if (pill) {
        pill.className = `status-pill ${status}`;
        pill.textContent = status.charAt(0).toUpperCase() + status.slice(1);
    }

    // Update data-status so the banner counter stays accurate
    row.dataset.status = status;

    // Replace action buttons with earnings summary (approved) or a note (rejected)
    const actionCell = row.querySelector('.action-cell');
    if (actionCell) {
        if (status === 'approved' && data) {
            actionCell.innerHTML = `
                <div class="earnings-details">
                    <small>⏱ ${data.work_hours}h worked &nbsp;|&nbsp; OT: ${data.overtime_hours}h</small><br>
                    <small>💰 KES ${data.total_pay.toLocaleString()} (reg: ${data.regular_pay.toLocaleString()} + OT: ${data.overtime_pay.toLocaleString()})</small>
                </div>`;
        } else if (status === 'rejected') {
            actionCell.innerHTML = `<span class="text-muted" style="font-size:.85rem;">Rejected</span>`;
        }
    }
}

function refreshPendingBanner() {
    const rows = document.querySelectorAll('#attendanceBody tr[data-id]');
    const pendingCount = Array.from(rows).filter(r => r.dataset.status === 'pending').length;

    const banner = document.getElementById('adminAlert');
    const text   = document.getElementById('pendingCountText');
    if (!banner) return;

    if (pendingCount > 0) {
        banner.style.display = 'flex';
        if (text) text.innerText = `${pendingCount} pending attendance record${pendingCount !== 1 ? 's' : ''}`;
    } else {
        banner.style.display = 'none';
    }
}

function filterTable(status) {
    document.querySelectorAll('#attendanceBody tr[data-id]').forEach(row => {
        row.style.display = (status === 'all' || row.dataset.status === status) ? '' : 'none';
    });
}

function manageActiveLink() {
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-item').forEach(link => {
        const href = link.getAttribute('href') || '';
        link.classList.toggle('active', currentPath.endsWith(href) && href !== '');
    });
}

document.addEventListener('DOMContentLoaded', function () {
    if (typeof window.API === 'undefined') {
        console.error('[attendance.js] window.API not found — load api.js first.');
        return;
    }
    refreshPendingBanner();
    manageActiveLink();
});
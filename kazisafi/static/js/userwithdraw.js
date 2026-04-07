// User Withdrawal JavaScript - Dynamic Backend Integration
document.addEventListener('DOMContentLoaded', function() {
    loadWithdrawalHistory();
    setupWithdrawalForm();
    setupQuickAmountButtons();
});

// Load withdrawal history from API
async function loadWithdrawalHistory() {
    try {
        const response = await API.call('/api/user-withdrawal-history/');
        if (response.status === 'success') {
            updateWithdrawalTable(response.data);
        }
    } catch (error) {
        console.error('Error loading withdrawal history:', error);
        // Fallback to template-rendered data
        updateWithdrawalStatsFromTemplate();
    }
}

// Update withdrawal table with dynamic data
function updateWithdrawalTable(withdrawals) {
    const tbody = document.getElementById('withdrawHistory');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    if (withdrawals.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="4" style="text-align: center; padding: 2rem;">
                    No withdrawal history found.
                </td>
            </tr>
        `;
        return;
    }
    
    withdrawals.forEach(withdrawal => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${API.formatDateTime(withdrawal.created_at)}</td>
            <td>${API.formatCurrency(withdrawal.amount)}</td>
            <td>${withdrawal.receipt_number || '--'}</td>
            <td>
                <span class="status-badge ${withdrawal.status}">
                    ${withdrawal.status.charAt(0).toUpperCase() + withdrawal.status.slice(1)}
                </span>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Setup withdrawal form with API integration
function setupWithdrawalForm() {
    const form = document.getElementById('withdrawalForm');
    const amountInput = document.getElementById('withdrawInput');
    const submitBtn = document.getElementById('withdrawBtn');
    
    if (form && amountInput && submitBtn) {
        form.addEventListener('submit', handleWithdrawalSubmit);
        
        // Real-time validation
        amountInput.addEventListener('input', validateAmount);
        
        // Set max amount based on available balance
        const maxLimitElement = document.getElementById('maxLimit');
        if (maxLimitElement) {
            const maxAmount = parseFloat(maxLimitElement.textContent.replace(/[^0-9.]/g, ''));
            amountInput.max = maxAmount;
        }
    }
}

// Handle withdrawal form submission
async function handleWithdrawalSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = document.getElementById('withdrawBtn');
    const formData = new FormData(form);
    
    // Validate amount
    const amount = parseFloat(formData.get('amount'));
    if (!amount || amount < 50) {
        API.showNotification('Minimum withdrawal amount is KES 50', 'error');
        return;
    }
    
    // Disable submit button
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" style="margin-right:8px">
                <circle cx="12" cy="12" r="10"/>
                <path d="M4 12 L16 12 M12 4 L12 20"/>
            </svg>
            Processing...
        `;
    }
    
    try {
        const response = await API.call('/api/process-withdrawal/', {
            method: 'POST',
            body: formData
        });
        
        if (response.status === 'success') {
            API.showNotification('Withdrawal request submitted successfully!', 'success');
            form.reset();
            loadWithdrawalHistory();
            updateBalanceDisplay();
        } else {
            API.showNotification(response.message || 'Failed to process withdrawal', 'error');
        }
    } catch (error) {
        API.showNotification('Error processing withdrawal', 'error');
        console.error('Withdrawal error:', error);
    } finally {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = `
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" style="margin-right:8px">
                    <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
                </svg>
                Withdraw to M-Pesa
            `;
        }
    }
}

// Setup quick amount buttons
function setupQuickAmountButtons() {
    const quickButtons = document.querySelectorAll('.quick-select button');
    const maxButton = document.querySelector('.max-btn');
    
    quickButtons.forEach(button => {
        if (!button.classList.contains('max-btn')) {
            const amount = parseInt(button.textContent.replace(/[^0-9]/g, ''));
            button.addEventListener('click', () => setAmount(amount));
        }
    });
    
    if (maxButton) {
        maxButton.addEventListener('click', setMaxAmount);
    }
}

// Set amount in input field
function setAmount(amount) {
    const amountInput = document.getElementById('withdrawInput');
    if (amountInput) {
        amountInput.value = amount;
        validateAmount();
    }
}

// Set maximum amount
function setMaxAmount() {
    const maxLimitElement = document.getElementById('maxLimit');
    const amountInput = document.getElementById('withdrawInput');
    
    if (maxLimitElement && amountInput) {
        const maxAmount = maxLimitElement.textContent.replace(/[^0-9.]/g, '');
        amountInput.value = maxAmount.replace('KES ', '').replace(',', '');
        validateAmount();
    }
}

// Validate withdrawal amount
function validateAmount() {
    const amountInput = document.getElementById('withdrawInput');
    const maxLimitElement = document.getElementById('maxLimit');
    
    if (!amountInput || !maxLimitElement) return;
    
    const amount = parseFloat(amountInput.value);
    const maxAmount = parseFloat(maxLimitElement.textContent.replace(/[^0-9.]/g, ''));
    
    // Remove previous validation styles
    amountInput.style.borderColor = '';
    
    if (amount > maxAmount) {
        amountInput.style.borderColor = '#ef4444';
        API.showNotification('Amount exceeds available balance', 'error');
        return false;
    }
    
    if (amount < 50) {
        amountInput.style.borderColor = '#f59e0b';
        API.showNotification('Minimum withdrawal is KES 50', 'error');
        return false;
    }
    
    return true;
}

// Update balance display
function updateBalanceDisplay() {
    // This would be updated via API response
    // For now, reload the page to show updated balance
    setTimeout(() => {
        window.location.reload();
    }, 2000);
}

// Fallback: Update stats from template-rendered data
function updateWithdrawalStatsFromTemplate() {
    const balanceElement = document.getElementById('displayBalance');
    const maxLimitElement = document.getElementById('maxLimit');
    
    // Get values from template if available
    if (balanceElement && balanceElement.textContent.trim() !== '') {
        // Values already rendered by Django template
        return;
    }
}

// Check withdrawal status
async function checkWithdrawalStatus(withdrawalId) {
    try {
        const response = await API.call(`/api/withdrawal-status/${withdrawalId}/`);
        if (response.status === 'success') {
            // Update the specific withdrawal in the table
            updateWithdrawalRow(withdrawalId, response.data);
        }
    } catch (error) {
        console.error('Error checking withdrawal status:', error);
    }
}

// Update specific withdrawal row
function updateWithdrawalRow(withdrawalId, data) {
    const rows = document.querySelectorAll('#withdrawHistory tr');
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        if (cells.length > 0) {
            const firstCell = cells[0].textContent;
            // Find the row that matches this withdrawal (simplified check)
            if (firstCell.includes(API.formatDateTime(data.created_at))) {
                const statusBadge = row.querySelector('.status-badge');
                if (statusBadge) {
                    statusBadge.textContent = data.status;
                    statusBadge.className = `status-badge ${data.status}`;
                }
            }
        }
    });
}

// Export withdrawal history
function exportWithdrawalHistory() {
    const rows = document.querySelectorAll('#withdrawHistory tr');
    let csv = 'Date & Time,Amount,Receipt Number,Status\n';
    
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        const rowData = Array.from(cells).map(cell => `"${cell.textContent}"`).join(',');
        csv += rowData + '\n';
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `withdrawal_history_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Real-time withdrawal status updates
function startWithdrawalStatusPolling() {
    setInterval(async () => {
        try {
            const response = await API.call('/api/withdrawal-updates/');
            if (response.status === 'success' && response.has_updates) {
                loadWithdrawalHistory();
            }
        } catch (error) {
            console.log('Real-time withdrawal updates not available');
        }
    }, 15000); // Check every 15 seconds
}

// Initialize real-time updates
document.addEventListener('DOMContentLoaded', function() {
    // Uncomment to enable real-time withdrawal status updates
    // startWithdrawalStatusPolling();
});

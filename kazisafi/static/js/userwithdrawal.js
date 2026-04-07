const EMP_DATA = { id: 'EMP001', dailyRate: 1500 };
let currentBalance = 0;

function syncBalance() {
    const attendance = JSON.parse(localStorage.getItem('attendanceRecords')) || [];
    const transactions = JSON.parse(localStorage.getItem('mpesaTransactions')) || [];

    const approved = attendance.filter(r => r.id === EMP_DATA.id && r.status === 'approved');
    const hourlyRate = EMP_DATA.dailyRate / 8;
    
    let totalEarned = 0;
    approved.forEach(day => {
        const ot = parseFloat(day.overtime) || 0;
        totalEarned += (EMP_DATA.dailyRate + (ot * hourlyRate));
    });

    const totalWithdrawn = transactions.filter(t => t.id === EMP_DATA.id)
                                      .reduce((sum, t) => sum + t.amount, 0);

    currentBalance = Math.max(0, totalEarned - totalWithdrawn);
    
    const display = document.getElementById('displayBalance');
    const maxLimitText = document.getElementById('maxLimit');
    
    if(display) display.innerText = `KES ${currentBalance.toLocaleString()}`;
    if(maxLimitText) maxLimitText.innerText = `KES ${currentBalance.toLocaleString()}`;
}

function setAmount(val) {
    const input = document.getElementById('withdrawInput');
    if(input) input.value = val;
}

function setMax() {
    const input = document.getElementById('withdrawInput');
    if(input) input.value = currentBalance;
}

function handleWithdraw() {
    const input = document.getElementById('withdrawInput');
    const amt = parseFloat(input.value);

    if (!amt || amt < 50) {
        alert("Minimum withdrawal is KES 50");
        return;
    }

    if (amt > currentBalance) {
        alert("Insufficient funds!");
        return;
    }

    const transactions = JSON.parse(localStorage.getItem('mpesaTransactions')) || [];
    
    const request = {
        id: EMP_DATA.id,
        amount: amt,
        receipt: "MPESA-" + Math.random().toString(36).toUpperCase().substring(2, 10),
        timestamp: new Date().toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false }),
        status: 'Completed'
    };

    transactions.push(request);
    localStorage.setItem('mpesaTransactions', JSON.stringify(transactions));

    alert(`KES ${amt.toLocaleString()} sent to M-Pesa successfully!`);
    input.value = '';
    
    syncBalance();
    renderHistory();
}

function renderHistory() {
    const transactions = JSON.parse(localStorage.getItem('mpesaTransactions')) || [];
    const myHistory = transactions.filter(t => t.id === EMP_DATA.id).reverse();
    
    const list = document.getElementById('withdrawHistory');
    if(!list) return;
    
    list.innerHTML = '';

    myHistory.forEach(t => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${t.timestamp}</td>
            <td style="font-weight:600">KES ${t.amount.toLocaleString()}</td>
            <td style="color:#6b7280; font-family:monospace">${t.receipt}</td>
            <td><span class="status-pill" style="background:#f0fdf4; color:#16a34a; padding:4px 10px; border-radius:12px; font-size:11px; font-weight:600;">${t.status}</span></td>
        `;
        list.appendChild(row);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    syncBalance();
    renderHistory();
});
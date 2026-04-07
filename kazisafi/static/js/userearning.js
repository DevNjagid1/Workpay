const currentEmployee = { id: 'EMP001', rate: 1500 };

function calculateEarnings() {
    const attendance = JSON.parse(localStorage.getItem('attendanceRecords')) || [];
    const transactions = JSON.parse(localStorage.getItem('mpesaTransactions')) || [];

    const approvedDays = attendance.filter(r => r.id === currentEmployee.id && r.status === 'approved');
    const myWithdrawals = transactions.filter(t => t.id === currentEmployee.id);

    const hourlyRate = currentEmployee.rate / 8;
    let totalGross = 0;

    const body = document.getElementById('earningsBody');
    body.innerHTML = '';

    approvedDays.forEach(day => {
        const otHrs = parseFloat(day.overtime) || 0;
        const otPay = otHrs * hourlyRate;
        const dayTotal = currentEmployee.rate + otPay;
        totalGross += dayTotal;

        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${day.date}</td>
            <td>${day.day}</td>
            <td>${otHrs} h</td>
            <td style="font-weight:600; color:#059669">KES ${dayTotal.toLocaleString()}</td>
        `;
        body.appendChild(row);
    });

    const totalWithdrawn = myWithdrawals.reduce((sum, w) => sum + w.amount, 0);
    const balance = Math.max(0, totalGross - totalWithdrawn);

    document.getElementById('daysWorked').innerText = approvedDays.length;
    document.getElementById('totalEarned').innerText = `KES ${totalGross.toLocaleString()}`;
    document.getElementById('availableBalance').innerText = `KES ${balance.toLocaleString()}`;

    document.getElementById('formulaText').innerText = 
        `Earnings = (${approvedDays.length} days × KES ${currentEmployee.rate.toLocaleString()}) + (${(totalGross - (approvedDays.length * currentEmployee.rate)).toLocaleString()} OT Pay) = KES ${totalGross.toLocaleString()}`;

    document.getElementById('calcTotal').innerText = `KES ${totalGross.toLocaleString()}`;
    document.getElementById('calcWithdrawn').innerText = `- KES ${totalWithdrawn.toLocaleString()}`;
    document.getElementById('calcBalance').innerText = `= KES ${balance.toLocaleString()}`;
}

document.addEventListener('DOMContentLoaded', calculateEarnings);
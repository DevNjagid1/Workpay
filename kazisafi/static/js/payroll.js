const employees = [
    { id: 'EMP001', name: 'Jane Wanjiku', rate: 1500 },
    { id: 'EMP002', name: 'Peter Omondi', rate: 1500 },
    { id: 'EMP003', name: 'Mary Akinyi', rate: 1800 },
    { id: 'EMP004', name: 'Samuel Kamau', rate: 1200 },
    { id: 'EMP005', name: 'Catherine Mutua', rate: 1500 },
    { id: 'EMP006', name: 'David Kiprono', rate: 1400 },
    { id: 'EMP007', name: 'Alice Njeri', rate: 1500 },
    { id: 'EMP008', name: 'John Otieno', rate: 1500 }
];

const mpesaTransactions = [
    { name: 'Peter Omondi', id: 'EMP002', amount: 1200, phone: '+254700100002', receipt: 'MPESA-DEF67890', date: 'Jan 30, 2026 10:15' },
    { name: 'Jane Wanjiku', id: 'EMP001', amount: 800, phone: '+254700100001', receipt: 'MPESA-ABC12345', date: 'Jan 28, 2026 14:30' }
];

let currentView = 'summary';

function renderView(filterText = '') {
    const head = document.getElementById('payrollHead');
    const body = document.getElementById('payrollBody');
    const attendanceRecords = JSON.parse(localStorage.getItem('attendanceRecords')) || [];

    body.innerHTML = '';
    
    if (currentView === 'summary') {
        head.innerHTML = `<tr><th>Employee</th><th>Daily Rate</th><th>OT Payment</th><th>Total Earned</th><th>Withdrawn</th><th>Balance</th></tr>`;
        
        let globalPayroll = 0;
        let globalWithdrawn = 0;

        employees.forEach(emp => {
            if (!emp.name.toLowerCase().includes(filterText.toLowerCase()) && !emp.id.toLowerCase().includes(filterText.toLowerCase())) return;

            const record = attendanceRecords.find(r => r.id === emp.id) || { overtime: 0 };
            const otHrs = parseFloat(record.overtime) || 0;
            const otPay = otHrs * (emp.rate / 8);
            const totalEarned = emp.rate + otPay;
            
            let withdrawn = mpesaTransactions
                .filter(tx => tx.id === emp.id)
                .reduce((sum, tx) => sum + tx.amount, 0);
            
            if (withdrawn > totalEarned) withdrawn = totalEarned;
            
            const balance = totalEarned - withdrawn;

            globalPayroll += totalEarned;
            globalWithdrawn += withdrawn;

            const row = document.createElement('tr');
            row.innerHTML = `
                <td>
                    <div class="user-cell">
                        <div class="avatar">${emp.id.slice(-2)}</div>
                        <div class="user-info-stack">
                            <strong>${emp.name}</strong>
                            <small>${emp.id}</small>
                        </div>
                    </div>
                </td>
                <td>KES ${emp.rate.toLocaleString()}</td>
                <td class="ot-amount">KES ${otPay.toFixed(2)}</td>
                <td class="total-earned">KES ${totalEarned.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                <td class="withdraw-amount">KES ${withdrawn.toLocaleString()}</td>
                <td class="balance-amount">KES ${balance.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
            `;
            body.appendChild(row);
        });

        document.getElementById('totalPayrollVal').innerText = `KES ${globalPayroll.toLocaleString()}`;
        document.getElementById('totalWithdrawnVal').innerText = `KES ${globalWithdrawn.toLocaleString()}`;
        document.getElementById('totalBalanceVal').innerText = `KES ${(globalPayroll - globalWithdrawn).toLocaleString()}`;
    } else {
        head.innerHTML = `<tr><th>Employee</th><th>Amount</th><th>Phone</th><th>Receipt</th><th>Date & Time</th></tr>`;
        mpesaTransactions.filter(tx => tx.name.toLowerCase().includes(filterText.toLowerCase())).forEach(tx => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>
                    <div class="user-cell">
                        <div class="avatar">${tx.id.slice(-2)}</div>
                        <div class="user-info-stack">
                            <strong>${tx.name}</strong>
                            <small>${tx.id}</small>
                        </div>
                    </div>
                </td>
                <td><strong>KES ${tx.amount.toLocaleString()}</strong></td>
                <td>${tx.phone}</td>
                <td>${tx.receipt}</td>
                <td>${tx.date}</td>
            `;
            body.appendChild(row);
        });
    }
}

document.getElementById('btnSummary').addEventListener('click', () => {
    currentView = 'summary';
    document.getElementById('btnSummary').classList.add('active');
    document.getElementById('btnMpesa').classList.remove('active');
    renderView();
});

document.getElementById('btnMpesa').addEventListener('click', () => {
    currentView = 'mpesa';
    document.getElementById('btnMpesa').classList.add('active');
    document.getElementById('btnSummary').classList.remove('active');
    renderView();
});

document.getElementById('employeeSearch').addEventListener('input', (e) => renderView(e.target.value));
document.addEventListener('DOMContentLoaded', () => renderView());

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

document.addEventListener('DOMContentLoaded', manageActiveLink);
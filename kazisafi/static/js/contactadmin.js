const EMP = { id: 'EMP001', name: 'Jane Wanjiku' };

function showTicketForm() {
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('ticketDetailContent').style.display = 'none';
    document.getElementById('ticketForm').style.display = 'block';
}

function hideTicketForm() {
    document.getElementById('emptyState').style.display = 'flex';
    document.getElementById('ticketForm').style.display = 'none';
    document.getElementById('ticketDetailContent').style.display = 'none';
}

function viewTicketDetails(ticketId) {
    const tickets = JSON.parse(localStorage.getItem('supportTickets')) || [];
    const ticket = tickets.find(t => t.id === ticketId);

    if (ticket) {
        document.getElementById('emptyState').style.display = 'none';
        document.getElementById('ticketForm').style.display = 'none';
        
        const detailContent = document.getElementById('ticketDetailContent');
        detailContent.style.display = 'block';
        detailContent.innerHTML = `
            <div class="detail-header">
                <span class="status-pill ${ticket.status}">${ticket.status === 'Open' ? 'Pending' : 'Addressed'}</span>
                <h3 style="margin-top:10px">${ticket.category}</h3>
                <small style="color:#9ca3af">${ticket.id} • Submitted on ${ticket.date}</small>
            </div>
            <div class="detail-body">
                <p>${ticket.message}</p>
            </div>
            <div class="detail-footer">
                <p>Resolution Status: <strong>${ticket.status === 'Open' ? 'Pending Review' : 'Addressed by Admin'}</strong></p>
                <p style="font-size:11px; color:#9ca3af; margin-top:5px">We aim to respond to all inquiries within 24 hours.</p>
            </div>
        `;
    }
}

function submitTicket() {
    const category = document.getElementById('ticketCategory').value;
    const msg = document.getElementById('ticketMessage').value;

    if (!msg) return alert("Please enter a message");

    const tickets = JSON.parse(localStorage.getItem('supportTickets')) || [];
    const newTkt = {
        id: `TKT-2026-${(tickets.length + 1).toString().padStart(4, '0')}`,
        employeeId: EMP.id,
        employeeName: EMP.name,
        category: category,
        message: msg,
        status: 'Open',
        date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    };

    tickets.push(newTkt);
    localStorage.setItem('supportTickets', JSON.stringify(tickets));
    document.getElementById('ticketMessage').value = '';
    hideTicketForm();
    renderPage();
}

function renderPage() {
    const tickets = JSON.parse(localStorage.getItem('supportTickets')) || [];
    const myTkts = tickets.filter(t => t.employeeId === EMP.id).reverse();
    
    document.getElementById('openCount').innerText = myTkts.filter(t => t.status === 'Open').length;
    document.getElementById('resolvedCount').innerText = myTkts.filter(t => t.status === 'Resolved').length;

    const list = document.getElementById('ticketList');
    list.innerHTML = '';

    myTkts.forEach(t => {
        const div = document.createElement('div');
        div.className = 'ticket-item';
        div.onclick = () => viewTicketDetails(t.id);
        div.innerHTML = `
            <div class="ticket-item-header">
                <span class="ticket-id">${t.id}</span>
                <span class="status-pill ${t.status}">${t.status === 'Open' ? 'Pending' : 'Addressed'}</span>
            </div>
            <h4>${t.category}</h4>
            <p>${t.message}</p>
        `;
        list.appendChild(div);
    });

    const path = window.location.pathname;
    const page = path.split("/").pop();
    document.querySelectorAll('.nav-item').forEach(link => {
        if(link.getAttribute('href') === page) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

document.addEventListener('DOMContentLoaded', renderPage);
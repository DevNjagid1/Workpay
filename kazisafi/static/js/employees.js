const modal = document.getElementById('employeeModal');
const openModalBtn = document.getElementById('openModalBtn');
const closeModal = document.getElementById('closeModal');
const employeeForm = document.getElementById('addEmployeeForm');
const employeeTableBody = document.querySelector('#employeeTable tbody');
const searchInput = document.getElementById('employeeSearch');

openModalBtn.addEventListener('click', () => modal.style.display = 'block');
closeModal.addEventListener('click', () => modal.style.display = 'none');
window.addEventListener('click', (e) => { if (e.target == modal) modal.style.display = 'none'; });

employeeForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const name = document.getElementById('newName').value;
    const id = document.getElementById('newId').value;
    const email = document.getElementById('newEmail').value;
    const phone = document.getElementById('newPhone').value;
    const rate = document.getElementById('newRate').value;
    const date = document.getElementById('newDate').value;
    const initials = name.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2);

    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td><div class="user-cell"><span class="avatar">${initials}</span><span>${name}</span></div></td>
        <td>${id}</td>
        <td>${email}</td>
        <td>${phone}</td>
        <td>KES ${parseInt(rate).toLocaleString()}</td>
        <td>${date}</td>
        <td><span class="badge active">Active</span></td>
        <td><button class="toggle-status-btn">Disable</button></td>
    `;
    employeeTableBody.appendChild(newRow);
    employeeForm.reset();
    modal.style.display = 'none';
});

document.addEventListener('click', function(e) {
    if (e.target.classList.contains('toggle-status-btn')) {
        const btn = e.target;
        const row = btn.closest('tr');
        const statusBadge = row.querySelector('.badge');
        
        if (btn.textContent === 'Disable') {
            statusBadge.textContent = 'Disabled';
            statusBadge.className = 'badge disabled';
            btn.textContent = 'Activate';
            btn.classList.add('activate');
        } else {
            statusBadge.textContent = 'Active';
            statusBadge.className = 'badge active';
            btn.textContent = 'Disable';
            btn.classList.remove('activate');
        }
    }
});

searchInput.addEventListener('keyup', function(e) {
    const term = e.target.value.toLowerCase();
    const rows = employeeTableBody.querySelectorAll('tr');
    rows.forEach(row => {
        row.style.display = row.innerText.toLowerCase().includes(term) ? '' : 'none';
    });
});

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
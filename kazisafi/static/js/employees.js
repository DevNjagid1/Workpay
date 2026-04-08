// Employee Management JavaScript - Works with Django template

document.addEventListener('DOMContentLoaded', function() {
    // Modal functionality
    const modal = document.getElementById('employeeModal');
    const openModalBtn = document.getElementById('openModalBtn');
    const closeModal = document.getElementById('closeModal');
    const employeeForm = document.getElementById('addEmployeeForm');
    const searchInput = document.getElementById('employeeSearch');

    // Open modal
    if (openModalBtn) {
        openModalBtn.addEventListener('click', function() {
            if (modal) modal.style.display = 'block';
        });
    }

    // Close modal
    if (closeModal) {
        closeModal.addEventListener('click', function() {
            if (modal) modal.style.display = 'none';
        });
    }

    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Handle form submission
    if (employeeForm) {
        employeeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const name = document.getElementById('newName').value;
            const id = document.getElementById('newId').value;
            const email = document.getElementById('newEmail').value;
            const phone = document.getElementById('newPhone').value;
            const rate = document.getElementById('newRate').value;
            const date = document.getElementById('newDate').value;

            // Simple validation
            if (!name || !id || !email || !phone || !rate || !date) {
                alert('Please fill all fields');
                return;
            }

            // Show success message (in real app, this would submit to Django)
            alert(`Employee ${name} would be created with ID: ${id}`);
            
            // Reset form and close modal
            employeeForm.reset();
            if (modal) modal.style.display = 'none';
            
            // In real app, you would refresh the page or update the table
            console.log('Employee data:', { name, id, email, phone, rate, date });
        });
    }

    // Search functionality
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const filterText = e.target.value.toLowerCase();
            const rows = document.querySelectorAll('#employeeTable tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filterText) ? '' : 'none';
            });
        });
    }

    // Toggle status buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('toggle-status-btn')) {
            const btn = e.target;
            const row = btn.closest('tr');
            const statusBadge = row.querySelector('.badge');
            
            if (btn.textContent === 'Disable') {
                statusBadge.textContent = 'Disabled';
                statusBadge.className = 'badge disabled';
                btn.textContent = 'Enable';
                btn.classList.add('enable');
            } else {
                statusBadge.textContent = 'Active';
                statusBadge.className = 'badge active';
                btn.textContent = 'Disable';
                btn.classList.remove('enable');
            }
        }
    });

    console.log('Employee management initialized');
});
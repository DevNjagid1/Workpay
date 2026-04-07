const navItems = document.querySelectorAll('.nav-item');
const logoutBtn = document.getElementById('logoutBtn');
const viewAllBtn = document.querySelector('.view-all');
const statCards = document.querySelectorAll('.stat-card');


if (viewAllBtn) {
    viewAllBtn.addEventListener('click', function(e) {
        e.preventDefault();
        const attendanceNav = Array.from(navItems).find(link => link.textContent === 'Attendance');
        if (attendanceNav) {
            attendanceNav.click();
        }
    });
}

if (logoutBtn) {
    logoutBtn.addEventListener('click', function() {
        if(confirm('Are you sure you want to log out?')) {
            window.location.reload();
        }
    });
}

statCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-2px)';
        card.style.transition = 'transform 0.2s ease';
    });
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0)';
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
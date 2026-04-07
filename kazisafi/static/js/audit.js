// Remove hardcoded audit logs - data will come from Django template

function renderLogs(filterText = '', typeFilter = 'all') {
    // Audit logs are rendered by Django template, no JavaScript rendering needed
    console.log('Audit logs rendered by Django template');
}

function filterLogs() {
    // This will be handled by Django view, not JavaScript
    console.log('Filter logs handled by Django view');
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
    renderLogs();
    manageActiveLink();
});

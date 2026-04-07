// Remove hardcoded tickets - data will come from Django template

function renderTickets(filter = 'all') {
    // Tickets are rendered by Django template, no JavaScript rendering needed
    console.log('Tickets rendered by Django template');
}

function filterTickets(status) {
    // This will be handled by Django view, not JavaScript
    console.log(`Filter tickets by status: ${status}`);
}

function viewTicket(id) {
    // This will be handled by Django view, not JavaScript
    console.log(`View ticket: ${id}`);
}

function resolveTicket(id) {
    // This will be handled by Django view, not JavaScript
    console.log(`Resolve ticket: ${id}`);
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
    renderTickets();
    manageActiveLink();
});

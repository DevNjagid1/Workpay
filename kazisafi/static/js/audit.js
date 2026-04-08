// audit.js — client-side search and filter
// Real-time filtering runs on the Django-rendered rows.
// The filterLogs() function is also defined inline in the template
// so it can be called by oninput/onchange attributes.
// This file is kept for any future extensions.

document.addEventListener('DOMContentLoaded', function () {
    // Active nav link
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-item').forEach(link => {
        const href = link.getAttribute('href') || '';
        link.classList.toggle('active', href !== '' && currentPath.includes(href));
    });
});
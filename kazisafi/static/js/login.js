// Login form handling for Django backend
const form = document.getElementById('loginForm');
const loginBtn = document.getElementById('loginBtn');
const forgotLink = document.getElementById('forgotPasswordLink');

// Let Django handle form submission - no JavaScript validation needed
// The form will submit to Django backend normally

forgotLink.addEventListener('click', (e) => {
    e.preventDefault();
    // Let Django handle password reset
    window.location.href = '/password-reset/';
});

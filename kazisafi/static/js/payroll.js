// payroll.js — tab switching and search
document.addEventListener('DOMContentLoaded', function () {
    const btnSummary  = document.getElementById('btnSummary');
    const btnMpesa    = document.getElementById('btnMpesa');
    const summaryView = document.getElementById('summaryView');
    const mpesaView   = document.getElementById('mpesaView');

    if (btnSummary && btnMpesa) {
        btnSummary.addEventListener('click', function () {
            btnSummary.classList.add('active');
            btnMpesa.classList.remove('active');
            if (summaryView) summaryView.style.display = '';
            if (mpesaView)   mpesaView.style.display   = 'none';
        });

        btnMpesa.addEventListener('click', function () {
            btnMpesa.classList.add('active');
            btnSummary.classList.remove('active');
            if (summaryView) summaryView.style.display = 'none';
            if (mpesaView)   mpesaView.style.display   = '';
        });
    }

    // Search filters whichever table is currently visible
    const searchInput = document.getElementById('employeeSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const term = this.value.toLowerCase();
            const activeBody = summaryView && summaryView.style.display !== 'none'
                ? document.getElementById('payrollBody')
                : document.getElementById('mpesaBody');
            if (!activeBody) return;
            activeBody.querySelectorAll('tr').forEach(row => {
                row.style.display = row.textContent.toLowerCase().includes(term) ? '' : 'none';
            });
        });
    }
});
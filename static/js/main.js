/* KongoBiz Main JavaScript */

document.addEventListener('DOMContentLoaded', function() {
  // Auto-dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(function(alert) {
    setTimeout(function() {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });

  // Add form-control class to form inputs that don't have it
  const formInputs = document.querySelectorAll('form input[type="text"], form input[type="email"], form input[type="url"], form input[type="number"], form textarea, form select');
  formInputs.forEach(function(input) {
    if (!input.classList.contains('form-control') && !input.classList.contains('form-select')) {
      if (input.tagName === 'SELECT') {
        input.classList.add('form-select');
      } else {
        input.classList.add('form-control');
      }
    }
  });

  // Confirm delete actions
  const deleteLinks = document.querySelectorAll('a[href*="supprimer"]');
  deleteLinks.forEach(function(link) {
    link.addEventListener('click', function(e) {
      if (!confirm('Etes-vous sur de vouloir supprimer?')) {
        e.preventDefault();
      }
    });
  });
});

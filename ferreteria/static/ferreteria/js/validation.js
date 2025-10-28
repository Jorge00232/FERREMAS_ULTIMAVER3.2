document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    var forms = document.getElementsByClassName('needs-validation');
    Array.prototype.filter.call(forms, function(form) {
        form.addEventListener('submit', function(event) {
            // Custom validation for email field
            var emailField = form.querySelector('input[type="email"]');
            if (emailField && !validateEmail(emailField.value)) {
                emailField.setCustomValidity("Correo electrónico no es válido");
            } else {
                emailField.setCustomValidity("");
            }

            if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    function validateEmail(email) {
        var re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        return re.test(String(email).toLowerCase());
    }
});

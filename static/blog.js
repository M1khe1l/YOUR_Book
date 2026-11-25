// Password hide/unhide script in 'registraton'
function togglePasswordVisibility() {
    const passwordField = document.getElementById("reg_password");
    const confirmField = document.getElementById("reg_confirm");
    const toggleIcon = document.getElementById("toggle-eye-icon");

    if (toggleIcon.classList.contains("fa-eye-slash")) {
        passwordField.type = "text";
        confirmField.type = "text";
        toggleIcon.classList.remove("fa-eye-slash");
        toggleIcon.classList.add("fa-eye");
    } else {
        passwordField.type = "password";
        confirmField.type = "password";
        toggleIcon.classList.remove("fa-eye");
        toggleIcon.classList.add("fa-eye-slash");
    }
}

// Password hide/unhide script in 'log_in'
function PasswordVisibility() {
    const passwordField = document.getElementById("log_password");
    const toggleIcon = document.getElementById("toggle-eye-icon");

    if (toggleIcon.classList.contains("fa-eye-slash")) {
        passwordField.type = "text";
        toggleIcon.classList.remove("fa-eye-slash");
        toggleIcon.classList.add("fa-eye");
    } else {
        passwordField.type = "password";
        toggleIcon.classList.remove("fa-eye");
        toggleIcon.classList.add("fa-eye-slash");
    }
}


// Scroll Up Arrow script
document.addEventListener("DOMContentLoaded", function () {
    const scrollToTopButton = document.getElementById("scrollToTop");

    // Show/hide button based on scroll position
    window.addEventListener("scroll", function () {
        if (window.scrollY > 800) {
            scrollToTopButton.style.display = "block";
        } else {
            scrollToTopButton.style.display = "none";
        }
    });

    // Scroll to top when button is clicked
    scrollToTopButton.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
});

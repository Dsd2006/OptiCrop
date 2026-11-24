
document.addEventListener("DOMContentLoaded", function () {

    // Mobile navigation
    const menuToggle = document.getElementById("menuToggle");
    const navLinks = document.querySelector(".nav-links");

    if (menuToggle && navLinks) {
        menuToggle.addEventListener("click", function () {
            navLinks.classList.toggle("show");
        });
    }

    // Close mobile menu after navigation
    document.querySelectorAll(".nav-links a").forEach(link => {
        link.addEventListener("click", function () {
            if (navLinks) navLinks.classList.remove("show");
        });
    });

    // Flash message close
    document.querySelectorAll(".flash-close").forEach(button => {
        button.addEventListener("click", function () {
            button.parentElement.remove();
        });
    });

    // Smooth reveal animation
    const revealElements = document.querySelectorAll(
        ".feature-card, .stat-card, .panel, .tip-card"
    );

    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.12
        });

        revealElements.forEach(element => {
            element.classList.add("reveal");
            observer.observe(element);
        });
    }

    // Prevent accidental double form submission
    const forms = document.querySelectorAll("form");

    forms.forEach(form => {
        form.addEventListener("reset", function () {
            const button = form.querySelector('button[type="submit"]');

            if (button) {
                button.disabled = false;
                button.innerHTML =
                    '<i data-lucide="sparkles"></i> Predict Suitable Crop';

                if (window.lucide) lucide.createIcons();
            }
        });
    });

});

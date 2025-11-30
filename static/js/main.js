document.addEventListener('DOMContentLoaded', () => {
    // CHATBOT SIDEBAR TOGGLE
    const orb = document.getElementById('chatbot-orb');
    const sidebar = document.getElementById('chatbot-sidebar');
    const closeBtn = document.getElementById('close-sidebar');

    if (orb && sidebar) {
        orb.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            if (sidebar) sidebar.classList.remove('open');
        });
    }

    // Close sidebar when clicking outside
    document.addEventListener('click', (e) => {
        if (sidebar && orb) {
            if (!sidebar.contains(e.target) && !orb.contains(e.target) && sidebar.classList.contains('open')) {
                sidebar.classList.remove('open');
            }
        }
    });

    // BUTTON HOVER EFFECTS
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            btn.style.transform = 'scale(1.05)';
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'scale(1)';
        });
    });

    // WELCOME TEXT FADE-IN
    const welcomeText = document.querySelector('.welcome-text');
    if (welcomeText) {
        welcomeText.style.opacity = '0';
        welcomeText.style.transform = 'translateY(20px)';
        setTimeout(() => {
            welcomeText.style.opacity = '1';
            welcomeText.style.transform = 'translateY(0)';
            welcomeText.style.transition = 'all 1s ease';
        }, 500);
    }

    // Auto-hide flash messages after 5 seconds
    document.querySelectorAll('.flash-message').forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            msg.style.transition = 'all 0.3s ease';
            setTimeout(() => msg.remove(), 300);
        }, 5000);
    });

    // Smooth OTP form submission (prevent default and use fetch for better UX)
    const emailForm = document.getElementById('email-form');
    const otpForm = document.getElementById('otp-form');

    if (emailForm) {
        emailForm.addEventListener('submit', function(e) {
            // Let it submit normally for now, but add loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
            }
        });
    }

    if (otpForm) {
        otpForm.addEventListener('submit', function(e) {
            // Let it submit normally for now, but add loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verifying...';
            }
        });
    }
});
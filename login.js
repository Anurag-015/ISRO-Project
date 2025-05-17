document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('.login-form');
    const signupLink = document.querySelector('.signup-link');
    const loginLink = document.querySelector('.login-link');
    const forgotPasswordLink = document.querySelector('.forgot-password-link');
    const resetPasswordLink = document.querySelector('.reset-password-link');

    const loginContainer = document.querySelector('.login-container');
    const signupContainer = document.querySelector('.signup-container');
    const forgotPasswordContainer = document.querySelector('.forgot-password-container');

    // Handle form submission
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const rememberMe = document.getElementById('remember-me').checked;

            // Simulate login API call
            console.log(`Login attempt: ${username}, Remember me: ${rememberMe}`);

            // Redirect to dashboard on successful login
            window.location.href = 'index.html';
        });
    }

    // Toggle between login and signup views
    if (signupLink) {
        signupLink.addEventListener('click', (e) => {
            e.preventDefault();
            loginContainer.style.display = 'none';
            signupContainer.style.display = 'block';
            forgotPasswordContainer.style.display = 'none';
        });
    }

    if (loginLink) {
        loginLink.addEventListener('click', (e) => {
            e.preventDefault();
            loginContainer.style.display = 'block';
            signupContainer.style.display = 'none';
            forgotPasswordContainer.style.display = 'none';
        });
    }

    // Toggle forgot password view
    if (forgotPasswordLink) {
        forgotPasswordLink.addEventListener('click', (e) => {
            e.preventDefault();
            loginContainer.style.display = 'none';
            signupContainer.style.display = 'none';
            forgotPasswordContainer.style.display = 'block';
        });
    }

    // Handle reset password
    if (resetPasswordLink) {
        resetPasswordLink.addEventListener('click', (e) => {
            e.preventDefault();
            const email = document.getElementById('reset-email').value;
            console.log(`Password reset requested for: ${email}`);
            alert('Password reset link has been sent to your email.');

            // Return to login view
            loginContainer.style.display = 'block';
            forgotPasswordContainer.style.display = 'none';
        });
    }
});

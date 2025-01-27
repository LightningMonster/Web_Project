// Display notification and auto-hide after 3 seconds
const notification = document.getElementById('notification');
if (notification) {
    notification.style.display = 'block';
    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
}

function showLoginMessage() {
    const message = document.getElementById('login-message');
    message.style.display = 'block';
    setTimeout(() => {
        message.style.display = 'none';
    }, 3000); // Hide after 3 seconds
}
// This is the menu toggle for the hamburger when signed in

document.addEventListener('DOMContentLoaded', function () {
    const hamburger = document.getElementById('hamburger');
    const menu = document.getElementById('user-menu');

    if (hamburger && menu) {
        hamburger.addEventListener('click', () => {
            menu.classList.toggle('active');
        });
    }
});

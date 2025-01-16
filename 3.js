// Get modal elements
const openFormButton = document.getElementById('open-login-form');
const modal = document.getElementById('login-modal');
const closeModalButton = document.querySelector('.close');

// Show the modal when the login/register button is clicked
openFormButton.addEventListener('click', (e) => {
  e.preventDefault();
  modal.style.display = 'flex';
});

// Hide the modal when the close button is clicked
closeModalButton.addEventListener('click', () => {
  modal.style.display = 'none';
});

// Hide the modal when clicking outside the modal content
window.addEventListener('click', (e) => {
  if (e.target === modal) {
    modal.style.display = 'none';
  }
});

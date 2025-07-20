// Simple form submission handler
const form = document.querySelector('form');
form.addEventListener('submit', (e) => {
  e.preventDefault();
  alert('Thanks for reaching out! I will get back to you soon.');
  form.reset();
});

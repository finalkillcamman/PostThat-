document.getElementById('year').textContent = new Date().getFullYear();
const form = document.getElementById('waitlist');
form.addEventListener('submit', function (event) {
  event.preventDefault();
  const note = document.getElementById('form-note');
  note.textContent = 'Thanks for your interest! The waitlist signup will be connected before public launch.';
  note.style.color = '#d4b4ff';
  form.reset();
});
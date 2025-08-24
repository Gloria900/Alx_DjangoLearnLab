// Run simple UX helpers after DOM loads
document.addEventListener("DOMContentLoaded", () => {
  // Example: auto-hide flash messages
  document.querySelectorAll(".alert[data-autohide]").forEach((el) => {
    setTimeout(() => el.remove(), 4000);
  });
});

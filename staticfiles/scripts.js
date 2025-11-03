// Universal page loading skeleton
window.addEventListener("load", () => {
  // Add delay for smoother fade-in (optional)
  setTimeout(() => {
    document.body.classList.add("loaded");
  }, 800); // 0.8 seconds
});

// Universal page loading skeleton with 3-second delay
window.addEventListener("load", () => {
  setTimeout(() => {
    document.body.classList.add("loaded"); // hides skeleton and shows content
  }, 3000); // 3000ms = 3 seconds
});

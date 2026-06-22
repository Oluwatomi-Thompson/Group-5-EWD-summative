/* ............................
   API BASE
   .......................... */
const API_BASE = "http://127.0.0.1:5000";

/* ............................
   BUTTONS (UNCHANGED)
  ............................ */
document.getElementById("applyBtn")?.addEventListener("click", () => {
  const btn = document.getElementById("applyBtn");

  btn.innerHTML = "Applying...";

  setTimeout(() => {
    btn.innerHTML = "Filters Applied";
  }, 1000);

  setTimeout(() => {
    btn.innerHTML = "Apply Filters";
  }, 2500);
});

document.getElementById("resetBtn")?.addEventListener("click", () => {
  location.reload();
});

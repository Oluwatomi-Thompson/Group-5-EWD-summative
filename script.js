/* ==========================================
   APPLY FILTER BUTTON
========================================== */

const applyBtn = document.getElementById("applyBtn");

/* APPLY FILTER ANIMATION */
applyBtn.addEventListener("click", () => {

  applyBtn.innerHTML = "Applying...";

  setTimeout(() => {
    applyBtn.innerHTML = "Filters Applied";
  }, 1000);

  setTimeout(() => {
    applyBtn.innerHTML = "Apply Filters";
  }, 2500);

});

/* ==========================================
   RESET BUTTON
========================================== */

const resetBtn = document.getElementById("resetBtn");

/* RELOAD PAGE */
resetBtn.addEventListener("click", () => {

  location.reload();

});

/* ==========================================
   SEARCH TABLE
========================================== */

const searchInput = document.getElementById("searchInput");

/* SEARCH FILTER */
searchInput.addEventListener("keyup", () => {

  const filter = searchInput.value.toLowerCase();

  const rows = document.querySelectorAll("#recordsTable tbody tr");

  rows.forEach((row) => {

    const text = row.textContent.toLowerCase();

    row.style.display = text.includes(filter)
      ? ""
      : "none";

  });

});

/* ==========================================
   SCROLL TO TOP
========================================== */

const scrollTopBtn = document.getElementById("scrollTopBtn");

/* SMOOTH SCROLL */
scrollTopBtn.addEventListener("click", () => {

  window.scrollTo({
    top: 0,
    behavior: "smooth"
  });

});

/* ==========================================
   DARK MODE TOGGLE
========================================== */

const themeToggle = document.getElementById("themeToggle");

/* TOGGLE LIGHT MODE */
themeToggle.addEventListener("click", () => {

  document.body.classList.toggle("light-mode");

});

/* ==========================================
   CHART DEFAULTS
========================================== */

Chart.defaults.color = "#b6c7e2";
Chart.defaults.borderColor = "#223d63";

/* ==========================================
   PAYMENT DONUT CHART
========================================== */

new Chart(
  document.getElementById("paymentChart"),
  {
    type: "doughnut",

    data: {

      labels: [
        "Credit Card",
        "Cash",
        "No Charge",
        "Unknown"
      ],

      datasets: [{

        data: [23, 25, 26, 26],

        backgroundColor: [
          "#3b82f6",
          "#36c2db",
          "#f8a900",
          "#f44343"
        ]

      }]
    },

    options: {

      responsive: true,

      maintainAspectRatio: false,

      cutout: "50%",

      plugins: {

        legend: {
          position: "bottom"
        }

      }

    }

  }
);
/* ==========================================
   API BASE
========================================== */
const API_BASE = "http://127.0.0.1:5000";

/* ==========================================
   APPLY FILTER BUTTON (UNCHANGED)
========================================== */
const applyBtn = document.getElementById("applyBtn");

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
   RESET BUTTON (UNCHANGED)
========================================== */
const resetBtn = document.getElementById("resetBtn");

resetBtn.addEventListener("click", () => {
  location.reload();
});

/* ==========================================
   SEARCH TABLE (UNCHANGED)
========================================== */
const searchInput = document.getElementById("searchInput");

searchInput.addEventListener("keyup", () => {
  const filter = searchInput.value.toLowerCase();

  const rows = document.querySelectorAll("#recordsTable tbody tr");

  rows.forEach((row) => {
    const text = row.textContent.toLowerCase();
    row.style.display = text.includes(filter) ? "" : "none";
  });
});

/* ==========================================
   SCROLL TOP (UNCHANGED)
========================================== */
const scrollTopBtn = document.getElementById("scrollTopBtn");

scrollTopBtn.addEventListener("click", () => {
  window.scrollTo({
    top: 0,
    behavior: "smooth"
  });
});

/* ==========================================
   DARK MODE (UNCHANGED)
========================================== */
const themeToggle = document.getElementById("themeToggle");

themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("light-mode");
});

/* ==========================================
   LOAD TRIPS FROM BACKEND
========================================== */
async function loadTrips() {
  try {
    const res = await fetch(`${API_BASE}/api/trips`);
    const trips = await res.json();

    const tbody = document.querySelector("#recordsTable tbody");
    tbody.innerHTML = "";

    trips.forEach(trip => {

  console.log(trip);

  tbody.innerHTML += `
    <tr>
      <td>${trip.trip_id ?? "N/A"}</td>
      <td>${trip.pickup_datetime ?? "N/A"}</td>
      <td>${trip.dropoff_datetime ?? "N/A"}</td>
      <td>${trip.pu_location_id ?? "N/A"}</td>
      <td>${trip.do_location_id ?? "N/A"}</td>
      <td>${trip.trip_distance ?? 0}</td>
      <td>${trip.fare_amount ?? 0}</td>
      <td>${trip.passenger_count ?? 1}</td>
      <td>${trip.payment_type ?? "Unknown"}</td>
    </tr>
  `;
    });
  } catch (err) {
    console.error("Trips error:", err);
  }
}

/* ==========================================
   LOAD STATS FROM BACKEND
========================================== */
async function loadStats() {
  try {
    const res = await fetch(`${API_BASE}/api/trips`);
    const trips = await res.json();

    const totalTrips = trips.length;

    const avgFare =
      trips.reduce((sum, t) => sum + (t.fare_amount || 0), 0) / totalTrips;

    const avgDistance =
      trips.reduce((sum, t) => sum + (t.trip_distance || 0), 0) / totalTrips;

    const cards = document.querySelectorAll(".stat-card h2");

    cards[0].innerText = totalTrips;
    cards[1].innerText = `$${avgFare.toFixed(2)}`;
    cards[2].innerText = `${avgDistance.toFixed(2)} mi`;

  } catch (err) {
    console.error("Stats error:", err);
  }
}

/* ==========================================
   PAYMENT CHART (SAFE VERSION)
========================================== */
let chartInstance = null;

async function loadChart() {
  try {
    const res = await fetch(`${API_BASE}/api/trips`);
    const data = await res.json();

    let cash = 0, card = 0, mobile = 0;

   data.forEach(t => {
  const method = (t.payment_method || "").toLowerCase();

  if (method === "cash") cash++;
  else if (method === "card") card++;
  else mobile++;
});

    const canvas = document.getElementById("paymentChart");
    if (!canvas) return;

    // destroy old chart if exists
    if (chartInstance) {
  chartInstance.destroy();
}

    window.chartInstance = new Chart(canvas, {
      type: "doughnut",
      data: {
        labels: ["Cash", "Card", "Mobile Money"],
datasets: [{
  data: [cash, card, mobile],
  backgroundColor: ["#3b82f6", "#36c2db", "#f8a900"]
}]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "50%",
        plugins: {
          legend: { position: "bottom" }
        }
      }
    });

  } catch (err) {
    console.error("Chart error:", err);
  }
}

/* ==========================================
   INIT APP
========================================== */
document.addEventListener("DOMContentLoaded", () => {
  loadTrips();
  loadStats();
  loadChart();
});
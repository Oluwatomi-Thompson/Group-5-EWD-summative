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

/* .............................
   SEARCH TABLE
.............................. */
document.getElementById("searchInput")?.addEventListener("keyup", () => {
  const filter = document.getElementById("searchInput").value.toLowerCase();

  const rows = document.querySelectorAll("#recordsTable tbody tr");

  rows.forEach((row) => {
    const text = row.textContent.toLowerCase();
    row.style.display = text.includes(filter) ? "" : "none";
  });
});

/* .............................
   SCROLL TOP
.............................. */
document.getElementById("scrollTopBtn")?.addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});

/* .............................
   DARK MODE
.............................. */
document.getElementById("themeToggle")?.addEventListener("click", () => {
  document.body.classList.toggle("light-mode");
});

/* .............................
   LOAD TRIPS
.............................. */
async function loadTrips() {
  try {
    const res = await fetch(`${API_BASE}/api/trips`);

    if (!res.ok) throw new Error("Failed to fetch trips");

    const trips = await res.json();

    const tbody = document.querySelector("#recordsTable tbody");
    if (!tbody) return;

    tbody.innerHTML = "";

    trips.forEach((trip) => {
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
          <td>${trip.payment_method ?? "Unknown"}</td>
        </tr>
      `;
    });

  } catch (err) {
    console.error("Trips error:", err);
  }
}

/* .............................
   LOAD STATS
.............................. */
async function loadStats() {
  try {
    const res = await fetch(`${API_BASE}/api/trips`);

    if (!res.ok) throw new Error("Failed to fetch stats");

    const trips = await res.json();

    const totalTrips = trips.length || 0;

    const avgFare =
      totalTrips > 0
        ? trips.reduce((sum, t) => sum + (t.fare_amount || 0), 0) / totalTrips
        : 0;

    const avgDistance =
      totalTrips > 0
        ? trips.reduce((sum, t) => sum + (t.trip_distance || 0), 0) / totalTrips
        : 0;

    const cards = document.querySelectorAll(".stat-card h2");

    if (cards.length >= 3) {
      cards[0].innerText = totalTrips;
      cards[1].innerText = `$${avgFare.toFixed(2)}`;
      cards[2].innerText = `${avgDistance.toFixed(2)} mi`;
    }

  } catch (err) {
    console.error("Stats error:", err);
  }
}

let chartInstance = null;

async function loadPaymentChart() {
  try {
    const res = await fetch(`${API_BASE}/api/trips`);

    if (!res.ok) throw new Error("Failed to fetch chart data");

    const trips = await res.json();

    let cash = 0;
    let card = 0;
    let mobile = 0;

    const paymentMap = {
      cash: "cash",
      card: "card",
      mobile: "mobile",
      "mobile money": "mobile",
      mtn: "mobile",
      airtel: "mobile",
      vodafone: "mobile"
    };

    trips.forEach((t) => {
      const method = paymentMap[String(t.payment_type || "").toLowerCase()] || "unknown";

      if (method === "cash") cash++;
      else if (method === "card") card++;
      else mobile++;
    });

    const canvas = document.getElementById("paymentChart");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    if (chartInstance) {
      chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
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

/* .............................
   INIT
.............................. */
document.addEventListener("DOMContentLoaded", () => {
  loadTrips();
  loadStats();
  loadPaymentChart();
});
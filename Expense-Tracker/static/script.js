// Date and Chart Modal Functionality

document.addEventListener("DOMContentLoaded", function() {
  // Date Modal Functionality
  var dateModal = document.getElementById("dateModal");
  var openDateModalBtn = document.getElementById("openDateModal");
  var dateModalClose = document.getElementById("dateModalClose");
  var dateForm = document.getElementById("dateForm");
  
  if (openDateModalBtn && dateModal) {
    openDateModalBtn.addEventListener("click", function() {
      dateModal.style.display = "block";
    });
  }
  if (dateModalClose && dateModal) {
    dateModalClose.addEventListener("click", function() {
      dateModal.style.display = "none";
    });
  }
  if (dateForm && dateModal) {
    dateForm.addEventListener("submit", function() {
      dateModal.style.display = "none";
    });
  }
  
  window.addEventListener("click", function(event) {
    if (event.target === dateModal) {
      dateModal.style.display = "none";
    }
    var chartModal = document.getElementById("chartModal");
    if (chartModal && event.target === chartModal) {
      chartModal.style.display = "none";
    }
  });
  
  // Chart Modal Functionality
  var chartModal = document.getElementById("chartModal");
  var chartModalClose = document.getElementById("chartModalClose");
  var enlargedChartCanvas = document.getElementById("enlargedChartCanvas");
  var chartTiles = document.getElementsByClassName("chart-tile");
  
  for (var i = 0; i < chartTiles.length; i++) {
    chartTiles[i].addEventListener("click", function() {
      if (chartModal) {
        chartModal.style.display = "block";
        // Initialize enlarged chart on modal canvas using window.chartData if available
        if (window.chartData && window.chartData.labels && window.chartData.values) {
          new Chart(enlargedChartCanvas.getContext("2d"), {
            type: "line",
            data: {
              labels: window.chartData.labels,
              datasets: [{
                label: "Total Expenses",
                data: window.chartData.values,
                backgroundColor: "rgba(128, 0, 128, 0.2)",
                borderColor: "rgba(128, 0, 128, 1)",
                borderWidth: 2,
                fill: true,
                tension: 0.4
              }]
            },
            options: {
              responsive: true,
              animation: { duration: 1500 },
              scales: { y: { beginAtZero: true } }
            }
          });
        }
      }
    });
  }
  
  if (chartModalClose && chartModal) {
    chartModalClose.addEventListener("click", function() {
      chartModal.style.display = "none";
    });
  }
});

document.addEventListener("alpine:init", () => {
    Alpine.data('app', () => ({
        selectedDigester: '',
        wasteVolume: null,
        showMessage: false,
        predictionResult: null,
        showTable: false, // Property for showing the comparison table
        history: [],
        chart: null,

        init() {
            // Load the prediction history from localStorage
            this.history = JSON.parse(localStorage.getItem('biogasHistory')) || [];
            
            // Use $nextTick to ensure the DOM is updated before attempting to access the canvas
            this.$nextTick(() => {
                const ctx = document.getElementById('historyChart').getContext('2d');
                if (ctx) {
                    this.renderChart(ctx);
                } else {
                    console.error("Canvas context not found");
                }
            });
        },

        renderChart() {
            setTimeout(() => {
              const canvas = document.getElementById('historyChart');
              const ctx = canvas?.getContext('2d');
          
              if (!ctx) {
                console.error("Canvas context not found");
                return;
              }
          
              canvas.style.display = '';
          
              const labels = this.history.map(entry => entry.date);
              const data = this.history.map(entry => parseFloat(entry.output));
          
              console.log('Creating chart with labels:', labels);
              console.log('Data:', data);
          
              if (data.length === 0 || data.every(isNaN)) {
                console.error("No valid data for chart");
                return;
              }
          
              if (this.chart) {
                this.chart.destroy(); // Destroy previous chart instance
              }
          
              try {
                this.chart = new Chart(ctx, {
                  type: 'bar',
                  data: {
                    labels: labels,
                    datasets: [{
                      label: 'Predicted Biogas Output (m³)',
                      data: data,
                      backgroundColor: 'rgba(75, 192, 192, 0.5)',
                      borderColor: 'rgba(75, 192, 192, 1)',
                      borderWidth: 2
                    }]
                  },
                  options: {
                    responsive: true,
                    scales: {
                      x: {
                        title: {
                          display: true,
                          text: 'Date'
                        }
                      },
                      y: {
                        beginAtZero: true,
                        title: {
                          display: true,
                          text: 'Predicted Output (m³)'
                        }
                      }
                    }
                  }
                });
          
                console.log('Chart created successfully', this.chart);
              } catch (error) {
                console.error("Error creating chart:", error);
              }
            }, 100);
        },
        

        clearHistory() {
            // Clear the history and remove from localStorage
            this.history = [];
            localStorage.removeItem('biogasHistory');

            // Clear the chart if it exists
            if (this.chart) {
                this.chart.destroy();
            }
        },

        // Select a digester and reset the table view
        selectDigester(digester) {
            this.selectedDigester = digester;
            this.showMessage = false; // Reset message when digester is selected
            this.showTable = false;   // Reset the table view when a new digester is selected
        },

        // Function to handle form submission
        submitForm() {
            if (this.selectedDigester && this.wasteVolume) {
                // Call the API to get the biogas prediction
                axios.post('http://127.0.0.1:5000/api/ml/predict', {
                    digester_type: this.selectedDigester,
                    total_waste: this.wasteVolume
                }, {
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => {
                    this.showMessage = true;
                    this.predictionResult = response.data[0][0]; // Assuming the prediction is returned in the first index

                    // Save the prediction to history
                    const predictionEntry = {
                        digester: this.selectedDigester,
                        wasteVolume: this.wasteVolume,
                        output: this.predictionResult,
                        date: new Date().toLocaleString()
                    };
                    this.history.push(predictionEntry);

                    // Save history to localStorage
                    localStorage.setItem('biogasHistory', JSON.stringify(this.history));

                    // Clear the form fields
                    this.selectedDigester = '';
                    this.wasteVolume = null;
                })
                .catch(error => {
                    console.error("Error making the API request:", error);
                    alert("Failed to get the prediction. Please try again.");
                });
            } else {
                alert("Please fill in all fields.");
            }
        }
    }));
});
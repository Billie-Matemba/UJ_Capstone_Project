document.addEventListener("alpine:init", () => {
    Alpine.data('app', () => ({
        selectedDigester: '',
        wasteVolume: null,
        showMessage: false,
        predictionResult: null,
        showTable: false, // Property for showing the comparison table

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
                    console.log("Prediction Result:", this.predictionResult);
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

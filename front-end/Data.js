document.addEventListener("alpine:init", () => {
    Alpine.data('app', () => ({
        // showTerms: true,
        // showBiogasInputs: false,
        // canContinue: false,
        digester: '',
        wasteVolume: null,
        showMessage: false,
        predictionResult: null, // For storing the prediction result

        // Accept the terms
        // agree() {
        //     this.canContinue = true;
        //     this.showTerms = false; // Hide terms and show biogas input form
        //     this.showBiogasInputs = true;
        //     alert('Thank you for accepting the terms.');
        // },

        // // Decline the terms
        // disagree() {
        //     this.canContinue = false;
        //     alert('You must agree to the terms to continue.');
        // },

        selectDigester(digesterType) {
            this.digester = digesterType;
        },

        // Submit the biogas form and send data to the API
        submitForm() {
            if (this.digester && this.wasteVolume) {
                // Call the API to get the biogas prediction
                axios.post('http://127.0.0.1:5000/api/ml/predict', {
                    digester_type: this.digester,  // Send the string value of digester
                    total_waste: this.wasteVolume
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

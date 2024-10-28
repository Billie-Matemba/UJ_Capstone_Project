from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
import numpy as np
from sklearn.preprocessing import LabelEncoder
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')


app = Flask(__name__, static_folder='./front-end')
CORS(app)
model = load_model('trained_model.keras')

# Load the LabelEncoder used during model training
le = LabelEncoder()
le.fit(['Covered Lagoon', 'Complete Mix', 'Mixed Plug Flow', 'Horizontal Plug Flow'])  

@app.route('/', methods=['GET'])
def home():
    return app.send_static_file('index.html')

@app.route('/api/ml/predict', methods=['POST'])
def predict():
    data = request.get_json()
    digester_type_str = data.get('digester_type')
    total_waste = float(data.get('total_waste'))

    # Encode the digester_type as integer
    digester_type_encoded = le.transform([digester_type_str])[0]
    
    # Prepare input for the model
    x_input = np.array([[digester_type_encoded, total_waste]])
    
    # Predict using the loaded model
    prediction = model.predict(x_input).tolist()
    
    return jsonify(prediction)

# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 10000))  
#     app.run(port=port, host='0.0.0.0')       

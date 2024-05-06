from flask import Flask, request, render_template
import pickle
import sys
import sklearn as sk
sys.modules['sklearn'] = sk


app = Flask(__name__)

# Load models
with open('best_model_day.pkl', 'rb') as f:
    model_day = pickle.load(f)
with open('best_model_night.pkl', 'rb') as f:
    model_night = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract features from the form
    features = [int(request.form.get('Year')), int(request.form.get('Month')),
                int(request.form.get('Name')), int(request.form.get('City')),
                int(request.form.get('State')), int(request.form.get('Type'))]
    
    # Choose model based on time of day (example: day vs night)
    model = model_day if request.form.get('Time') == 'day' else model_night
    
    # Predict
    prediction = model.predict([features])
    
    # Output prediction
    return render_template('index.html', prediction_text='Future trend prediction is: {}'.format(prediction[0]))

if __name__ == "__main__":
    app.run(debug=True)

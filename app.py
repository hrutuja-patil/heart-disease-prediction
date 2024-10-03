from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)
model_rf = joblib.load('heart_disease.pkl')

cp_mapping = {'typical_angina': 0, 'atypical_angina': 1, 'non_anginal_pain': 2, 'asymptomatic': 3}
restecg_mapping = {'normal': 0, 'having_ST-T_wave_abnormality': 1, 'showing_probable_or_definite_left_ventricular_hypertrophy': 2}
slope_mapping = {'upsloping': 0, 'flat': 1, 'downsloping': 2}
thal_mapping = {'normal': 0, 'fixed_defect': 1, 'reversable_defect': 2}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    
    features = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']


    user_input = {}
    for feature in features:
        value = request.form[feature]
        if feature in ['cp', 'restecg', 'slope', 'thal']:
            if feature == 'cp':
                user_input[feature] = [cp_mapping.get(value, -1)]
            elif feature == 'restecg':
                user_input[feature] = [restecg_mapping.get(value, -1)]
            elif feature == 'slope':
                user_input[feature] = [slope_mapping.get(value, -1)]
            elif feature == 'thal':
                user_input[feature] = [thal_mapping.get(value, -1)]
        else:
            try:
                user_input[feature] = [float(value)]
            except ValueError:
                return "Invalid input: Please enter valid numerical values for all fields."

    user_DF = pd.DataFrame(user_input)

    try:
        pred_user = model_rf.predict(user_DF)
    except Exception as e:
        return f"An error occurred during prediction: {e}"
    return render_template('result.html', result=pred_user[0])

if __name__ == '__main__':
    app.run(debug=True)

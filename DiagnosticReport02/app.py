from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load the dataset
data = pd.read_csv('D:\DiagnosticReport02\PatientRandom - Sheet2 (2).csv')

# Preprocess the data
label_encoder_diagnosis = LabelEncoder()
label_encoder_heart = LabelEncoder()
label_encoder_blood_sugar = LabelEncoder()

data['heart_diagnosis'] = label_encoder_heart.fit_transform(data['heart_diagnosis'])
data['blood_sugar_diagnosis'] = label_encoder_blood_sugar.fit_transform(data['blood_sugar_diagnosis'])
data['diagnosis'] = label_encoder_diagnosis.fit_transform(data['diagnosis'])

# Split the data into X and y
X = data[['cholesterol_level_mg', 'heart_rate_bpm', 'blood_sugar_level_mg']]
y_diagnosis = data['diagnosis']
y_heart_diagnosis = data['heart_diagnosis']
y_blood_sugar_diagnosis = data['blood_sugar_diagnosis']

# Create and fit the models
diagnosis_model = RandomForestClassifier(n_estimators=100)
diagnosis_model.fit(X, y_diagnosis)

heart_model = RandomForestClassifier(n_estimators=100)
heart_model.fit(X[['heart_rate_bpm']], y_heart_diagnosis)

blood_sugar_model = RandomForestClassifier(n_estimators=100)
blood_sugar_model.fit(X[['blood_sugar_level_mg']], y_blood_sugar_diagnosis)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    name = request.form['name']
    
    patient_data = data[data['name'] == name]
    if patient_data.empty:
        error_message = "Patient not found in the dataset."
        return render_template('index.html', error_message=error_message)
    
    patient_name = patient_data['name'].values[0]
    
    if 'diagnosis' in request.form:
        # Make diagnosis prediction
        diagnosis_labels = label_encoder_diagnosis.classes_
        diagnosis_prediction = label_encoder_diagnosis.inverse_transform(
            diagnosis_model.predict(patient_data[['cholesterol_level_mg', 'heart_rate_bpm', 'blood_sugar_level_mg']])
        )
        return render_template('index.html',
                               patient_name=patient_name,
                               diagnosis_prediction=diagnosis_prediction[0],
                               diagnosis_labels=diagnosis_labels)
    
    if 'heart_diagnosis' in request.form:
        # Make heart diagnosis prediction
        heart_diagnosis_labels = label_encoder_heart.classes_
        heart_diagnosis_prediction = label_encoder_heart.inverse_transform(
            heart_model.predict(patient_data[['heart_rate_bpm']])
        )
        return render_template('index.html',
                               patient_name=patient_name,
                               heart_diagnosis_prediction=heart_diagnosis_prediction[0],
                               heart_diagnosis_labels=heart_diagnosis_labels)
    
    if 'blood_sugar_diagnosis' in request.form:
        # Make blood sugar diagnosis prediction
        blood_sugar_diagnosis_labels = label_encoder_blood_sugar.classes_
        blood_sugar_diagnosis_prediction = label_encoder_blood_sugar.inverse_transform(
            blood_sugar_model.predict(patient_data[['blood_sugar_level_mg']])
        )
        return render_template('index.html',
                               patient_name=patient_name,
                               blood_sugar_diagnosis_prediction=blood_sugar_diagnosis_prediction[0],
                               blood_sugar_diagnosis_labels=blood_sugar_diagnosis_labels)
    
    error_message = "Invalid prediction request."
    return render_template('index.html', error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)

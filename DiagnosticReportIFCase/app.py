from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the dataset
data = pd.read_csv('D:\DiagnosticReportIFCase\PatientRandom - Sheet4.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the patient name from the form
        name = request.form['name']

        # Filter the dataset based on the patient name
        patient_data = data[data['Name'] == name]

        if patient_data.empty:
            error_message = "Patient not found in the dataset."
            return render_template('index.html', error_message=error_message)

        # Count the occurrences of each diagnosis for the patient
        diagnosis_counts = patient_data['Diagnosis'].value_counts()

        # Calculate the percentages
        diagnosis_percentages = diagnosis_counts / diagnosis_counts.sum() * 100

        # Get the top three diagnoses
        top_three_diagnoses = diagnosis_percentages.head(3)

        return render_template('index.html', name=name, diagnoses=zip(top_three_diagnoses.index, top_three_diagnoses.values))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)

# Load and preprocess the dataset
data = pd.read_csv('D:\DiagnosticReport\PatientRandom - Sheet2.csv')
df = pd.DataFrame(data)

label_encoder = LabelEncoder()
df['Diagnosis_Encoded'] = label_encoder.fit_transform(df['Diagnosis'])

X = df[['Cholesterol Level mg/dL', 'Heart Rate bpm', 'Blood Sugar Level mg/dL']]
y = df['Diagnosis_Encoded']

# Train the model
model = RandomForestClassifier()
model.fit(X, y)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    person_name = request.form['name']
    person_data = df[df['Name'] == person_name]

    if person_data.empty:
        message = 'Person not found in the dataset.'
        return render_template('index.html', message=message, diagnosis=None, graph_data=None)

    person_data = person_data.sort_values('Check-Ups')

    # Create a separate DataFrame for graph and analysis
    graph_data = person_data[['Check-Ups', 'Cholesterol Level mg/dL', 'Heart Rate bpm', 'Blood Sugar Level mg/dL']].copy()

    person_features = person_data[['Cholesterol Level mg/dL', 'Heart Rate bpm', 'Blood Sugar Level mg/dL']]
    diagnosis_encoded = model.predict(person_features)
    diagnosis = label_encoder.inverse_transform(diagnosis_encoded)[0]

    # Generate line graphs for each measurement
    plt.figure(figsize=(10, 6))

    plt.subplot(3, 1, 1)
    plt.plot(graph_data['Check-Ups'], graph_data['Cholesterol Level mg/dL'], marker='o', linestyle='-', markersize=4)
    plt.xlabel('Check-Ups')
    plt.ylabel('Cholesterol Level')
    plt.title(f'Cholesterol Level for {person_name}')
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(graph_data['Check-Ups'], graph_data['Heart Rate bpm'], marker='o', linestyle='-', markersize=4)
    plt.xlabel('Check-Ups')
    plt.ylabel('Heart Rate')
    plt.title(f'Heart Rate for {person_name}')
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(graph_data['Check-Ups'], graph_data['Blood Sugar Level mg/dL'], marker='o', linestyle='-', markersize=4)
    plt.xlabel('Check-Ups')
    plt.ylabel('Blood Sugar Level')
    plt.title(f'Blood Sugar Level for {person_name}')
    plt.grid(True)

    plt.tight_layout()

    # Save the graph as a base64 string
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_data_encoded = base64.b64encode(buffer.getvalue()).decode()
    plt.close()

    # Calculate analysis of health measurements
    cholesterol_mean = person_data['Cholesterol Level mg/dL'].mean()
    cholesterol_min = person_data['Cholesterol Level mg/dL'].min()
    cholesterol_max = person_data['Cholesterol Level mg/dL'].max()

    heart_rate_mean = person_data['Heart Rate bpm'].mean()
    heart_rate_min = person_data['Heart Rate bpm'].min()
    heart_rate_max = person_data['Heart Rate bpm'].max()

    blood_sugar_mean = person_data['Blood Sugar Level mg/dL'].mean()
    blood_sugar_min = person_data['Blood Sugar Level mg/dL'].min()
    blood_sugar_max = person_data['Blood Sugar Level mg/dL'].max()

    return render_template(
        'index.html',
        diagnosis=diagnosis,
        message=None,
        person_name=person_name,
        graph_data=graph_data_encoded,
        cholesterol_mean=cholesterol_mean,
        cholesterol_min=cholesterol_min,
        cholesterol_max=cholesterol_max,
        heart_rate_mean=heart_rate_mean,
        heart_rate_min=heart_rate_min,
        heart_rate_max=heart_rate_max,
        blood_sugar_mean=blood_sugar_mean,
        blood_sugar_min=blood_sugar_min,
        blood_sugar_max=blood_sugar_max
    )

if __name__ == '__main__':
    app.run(port=3000, debug=True)

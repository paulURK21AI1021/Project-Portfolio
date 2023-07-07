from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Load the dataset
data = pd.read_csv('D:\DiagnosticReport02\PatientRandom - Sheet2 (2).csv')

@app.route('/')
def index():
    return render_template('indexs.html')


@app.route('/plot', methods=['POST'])
def plot():
    name = request.form['name']
    
    # Fetch the data for the entered person
    person_data = data[data['name'] == name]
    
    if person_data.empty:
        error_message = "Person not found in the dataset."
        return render_template('indexs.html', error_message=error_message)
    
    # Get the required data for the line graph
    cholesterol_data = person_data['cholesterol_level_mg']
    heart_rate_data = person_data['heart_rate_bpm']
    blood_sugar_data = person_data['blood_sugar_level_mg']
    
    # Create the line graph
    fig, ax = plt.subplots()
    ax.plot(cholesterol_data, label='Cholesterol Level')
    ax.plot(heart_rate_data, label='Heart Rate')
    ax.plot(blood_sugar_data, label='Blood Sugar Level')
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.set_title('Health Data')
    ax.legend()
    
    # Save the graph to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Encode the buffer to base64 string
    graph_image = base64.b64encode(buffer.getvalue()).decode()
    
    plt.clf()  # Clear the plot for the next request
    
    return render_template('indexs.html', graph_image=graph_image)


if __name__ == '__main__':
    app.run(debug=True)

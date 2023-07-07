from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)   
data = pd.read_csv('D:\DiagnosticReportDateGen\PatientRandom - Sheet5.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        patients = data[data['AppointmentDate'] == date]['Name'].tolist()
        return render_template('index.html', patients=patients, date=date)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

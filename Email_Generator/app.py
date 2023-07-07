import csv
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Define an empty dictionary to store the email templates
email_templates = {}


def load_email_templates():
    with open('D:\Email_Generator\email_templates - Sheet1.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            keyword = row['Keyword']
            email_template = row['Email']
            email_templates[keyword] = email_template

load_email_templates()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-email', methods=['POST'])
def generate_email():
    keyword = request.form['keyword']
    if keyword not in email_templates:
        return render_template('index.html', error='Invalid keyword')

    email_template = email_templates[keyword]
    recipient_name = request.form['recipient_name']
    job_title = request.form['job_title']
    company_name = request.form['company_name']

    email_content = email_template.replace('[Candidate\'s Name]', recipient_name)
    email_content = email_content.replace('[Job Title]', job_title)
    email_content = email_content.replace('[Company Name]', company_name)

    return render_template('index.html', email=email_content)

if __name__ == '__main__':
    app.run(debug=True)

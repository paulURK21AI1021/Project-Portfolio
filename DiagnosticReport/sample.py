import pandas as pd
import matplotlib.pyplot as plt

# Create a sample dataframe
data = {
    'Name': ['John', 'Jane', 'Alice', 'Bob'],
    'Check-Ups': [1, 2, 3, 4],
    'Cholesterol Level mg/dL': [200, 180, 220, 190],
    'Heart Rate bpm': [70, 75, 80, 72],
    'Blood Sugar Level mg/dL': [100, 110, 95, 105]
}

df = pd.DataFrame(data)

# Get user input for name
person_name = input("Enter person's name: ")

# Filter dataframe based on user input
person_data = df[df['Name'] == person_name]

# Check if person exists in the dataframe
if person_data.empty:
    print('Person not found in the dataset.')
else:
    # Generate the graph
    plt.figure(figsize=(10, 6))

    plt.plot(person_data['Check-Ups'], person_data['Cholesterol Level mg/dL'], marker='o', linestyle='-', markersize=4, label='Cholesterol Level')
    plt.plot(person_data['Check-Ups'], person_data['Heart Rate bpm'], marker='o', linestyle='-', markersize=4, label='Heart Rate')
    plt.plot(person_data['Check-Ups'], person_data['Blood Sugar Level mg/dL'], marker='o', linestyle='-', markersize=4, label='Blood Sugar Level')

    plt.xlabel('Check-Ups')
    plt.ylabel('Measurement')
    plt.title(f'Measurements for {person_name}')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

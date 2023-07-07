import urllib.request
import zipfile
import os

# Define the URL and file name for the dataset
url = "https://www.dropbox.com/s/0w4tdebho0g1bbs/balanced_filtered_FER2013.zip?"
file_name = "balanced_filtered_FER2013.zip"

# Define the directory to extract the dataset
extract_dir = "D:\CNN_BS\zipExtracts"

# Download the dataset from the provided URL
urllib.request.urlretrieve(url, file_name)

# Extract the dataset
with zipfile.ZipFile(file_name, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# Delete the zip file
os.remove(file_name)

# Proceed with building the CNN model for emotion detection
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

# Step 1: Data Loading and Preprocessing
data_dir = "path_to_extracted_dataset"
image_height, image_width = 48, 48
num_channels = 1
num_classes = 7

# Load the dataset
train_data = np.load(os.path.join(data_dir, "train_data.npy"))
train_labels = np.load(os.path.join(data_dir, "train_labels.npy"))
test_data = np.load(os.path.join(data_dir, "test_data.npy"))
test_labels = np.load(os.path.join(data_dir, "test_labels.npy"))

# Normalize pixel values to the range of 0-1
train_data = train_data / 255.0
test_data = test_data / 255.0

# Reshape data to match the input shape of the model
train_data = train_data.reshape(-1, image_height, image_width, num_channels)
test_data = test_data.reshape(-1, image_height, image_width, num_channels)

# Convert labels to one-hot encoding
train_labels = tf.keras.utils.to_categorical(train_labels, num_classes)
test_labels = tf.keras.utils.to_categorical(test_labels, num_classes)

# Step 2: Model Architecture
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(image_height, image_width, num_channels)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(num_classes, activation='softmax'))

# Step 3: Model Compilation and Training
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(train_data, train_labels, epochs=10, batch_size=64, validation_data=(test_data, test_labels))

# Step 4: Model Evaluation
test_loss, test_accuracy = model.evaluate(test_data, test_labels)
print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")


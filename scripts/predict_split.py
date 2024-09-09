import tensorflow as tf
import numpy as np
import os
import shutil

label_to_index = {"None": 0, "Low": 1, "Medium": 2, "High": 3}
index_to_label = {v: k for k, v in label_to_index.items()}


def load_model(model_path="models/pistachio_model.h5"):
    return tf.keras.models.load_model(model_path)


def preprocess_image(image_path):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [224, 224])
    image = image / 255.0
    image = tf.expand_dims(image, axis=0)
    return image


def predict_split(model, image_path):
    image = preprocess_image(image_path)
    predictions = model.predict(image)
    predicted_label = np.argmax(predictions, axis=1)[0]
    return index_to_label[predicted_label]


def classify_and_allocate_images(model, new_images_dir):
    results = {"None": 0, "Low": 0, "Medium": 0, "High": 0}

    # Create directories for each split type if they don't exist
    for category in results.keys():
        os.makedirs(os.path.join(new_images_dir, category), exist_ok=True)

    for image_file in os.listdir(new_images_dir):
        if image_file.endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(new_images_dir, image_file)
            predicted_label = predict_split(model, image_path)
            results[predicted_label] += 1

            # Move the image to the corresponding folder
            new_path = os.path.join(new_images_dir, predicted_label, image_file)
            shutil.move(image_path, new_path)

    return results

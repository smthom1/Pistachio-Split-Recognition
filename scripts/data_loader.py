import os
import json
import tensorflow as tf
from sklearn.model_selection import train_test_split


def load_data(annotation_file, images_dir):
    with open(annotation_file, "r") as f:
        data = json.load(f)

    label_to_index = {"None": 0, "Low": 1, "Medium": 2, "High": 3}

    image_paths = []
    labels = []
    for annotation in data["annotations"]:
        image_id = annotation["image_id"]
        image_file = next(
            (img["file_name"] for img in data["images"] if img["id"] == image_id), None
        )
        if image_file:
            severity = annotation["attributes"]["Severity"]
            image_paths.append(os.path.join(images_dir, image_file))
            labels.append(label_to_index[severity])

    train_paths, val_paths, train_labels, val_labels = train_test_split(
        image_paths, labels, test_size=0.2, random_state=42
    )
    return train_paths, val_paths, train_labels, val_labels


def preprocess_image(image_path, label):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [224, 224])
    image = image / 255.0
    return image, label


def create_datasets(train_paths, val_paths, train_labels, val_labels, batch_size=32):
    # Create a TensorFlow dataset from paths and labels
    train_dataset = tf.data.Dataset.from_tensor_slices((train_paths, train_labels))
    val_dataset = tf.data.Dataset.from_tensor_slices((val_paths, val_labels))

    # Map the preprocessing function to the datasets
    train_dataset = train_dataset.map(preprocess_image).batch(batch_size)
    val_dataset = val_dataset.map(preprocess_image).batch(batch_size)

    return train_dataset, val_dataset

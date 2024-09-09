import os
import tensorflow as tf
from tensorflow.keras.layers import Input
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"


def build_model(input_shape=(224, 224, 3), num_classes=4):
    model = tf.keras.models.Sequential(
        [
            Input(shape=input_shape),
            tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(128, (3, 3), activation="relu"),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(512, activation="relu"),
            tf.keras.layers.Dense(num_classes, activation="softmax"),
        ]
    )
    return model


def train_model(
    train_dataset, val_dataset, epochs=10, model_save_path="models/pistachio_model.h5"
):
    model = build_model()
    model.compile(
        optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )

    history = model.fit(train_dataset, epochs=epochs, validation_data=val_dataset)

    final_accuracy = history.history["accuracy"][-1]
    final_val_accuracy = history.history["val_accuracy"][-1]
    final_loss = history.history["loss"][-1]
    final_val_loss = history.history["val_loss"][-1]

    print(f"Final Training Accuracy: {final_accuracy}")
    print(f"Final Validation Accuracy: {final_val_accuracy}")
    print(f"Final Training Loss: {final_loss}")
    print(f"Final Validation Loss: {final_val_loss}")

    model.save(model_save_path, save_format="tf")

    # Collect predictions and true labels for the validation set
    val_labels = []
    val_preds = []
    for images, labels in val_dataset:
        preds = model.predict(images)
        val_labels.extend(labels.numpy())
        val_preds.extend(preds)

    return model, val_labels, val_preds


def plot_roc_curve(y_true, y_pred, num_classes=4):
    fpr = {}
    tpr = {}
    roc_auc = {}

    for i in range(num_classes):
        fpr[i], tpr[i], _ = roc_curve(
            [1 if y == i else 0 for y in y_true], [p[i] for p in y_pred]
        )
        roc_auc[i] = auc(fpr[i], tpr[i])

    plt.figure()
    for i in range(num_classes):
        plt.plot(
            fpr[i], tpr[i], label=f"ROC curve (class {i}) (area = {roc_auc[i]:.2f})"
        )

    plt.plot([0, 1], [0, 1], "k--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Receiver Operating Characteristic (ROC) Curve")
    plt.legend(loc="lower right")
    plt.show()

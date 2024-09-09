import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
from scripts.data_loader import load_data, create_datasets
from scripts.train_model import train_model, plot_roc_curve
from scripts.predict_split import load_model, classify_and_allocate_images

# Paths
annotation_file = "data/annotations/instances_default.json"
images_dir = "data/images/"
new_images_dir = "new_images/"
model_save_path = "models/pistachio_model.h5"

# Step 1: Load and preprocess data
train_paths, val_paths, train_labels, val_labels = load_data(
    annotation_file, images_dir
)
train_dataset, val_dataset = create_datasets(
    train_paths, val_paths, train_labels, val_labels
)

# Step 2: Train the model
model, val_labels, val_preds = train_model(
    train_dataset, val_dataset, epochs=10, model_save_path=model_save_path
)

# Plot the ROC curve
plot_roc_curve(val_labels, val_preds)

# Step 3: Classify and allocate new images
model = load_model(model_save_path)
results = classify_and_allocate_images(model, new_images_dir)
for category, count in results.items():
    print(f"{category}: {count} images")

# Pistachio Split Recognition Project

This project trains a machine learning model to classify pistachio images based on split types (None, Low, Medium, High) and uses the trained model to classify new images.

## Table of Contents

- [Project Structure](#project-structure)
- [Setup and Usage](#setup-and-usage)
- [Explanation of Components](#explanation-of-components)
- [Modifying the Project](#modifying-the-project)

## Project Structure

pistachio_split_recognition/  
├── data/  
│ ├── images/  
│ └── annotations/  
├── scripts/  
│ ├── data_loader.py  
│ ├── train_model.py  
│ └── predict_split.py  
├── models/  
│ └── pistachio_model.h5  
├── new_images/  
└── main.py

### Description of Folders and Files

- **data/**: Contains the training dataset and annotations.
  - **images/**: Holds all the images used for training the model.
  - **annotations/**: Contains the `instances_default.json` file with labels for each image.
- **scripts/**: Contains the Python scripts for data loading, model training, and image classification.
  - **data_loader.py**: Loads and preprocesses the data, prepares datasets for training and validation.
  - **train_model.py**: Builds and trains the model, applies data augmentation.
  - **predict_split.py**: Uses the trained model to classify new images and organizes them into folders.
- **models/**: Stores the trained model.
  - **pistachio_model.h5**: The saved trained model file.
- **new_images/**: Contains new images to classify using the trained model.
- **main.py**: The main script to run the entire process (loading data, training the model, classifying new images).

## Setup and Usage

### 1. Prepare Data

1. Place your training images in the `data/images/` folder.
2. Ensure the `instances_default.json` file in `data/annotations/` correctly annotates these images.

### 2. Train the Model

Run the `main.py` script to train the model using the images and annotations in the `data/` folder. This will save the trained model in the `models/` folder.

```sh
python main.py
```

### 3. Classify New Images

1. Place new images in the `new_images/` folder.
2. Run the `main.py` script again to classify these images. The script will use the trained model to predict the split type for each new image and move it to the appropriate folder.

```sh
python main.py
```

## Explanation of Components

### For General Audience

- **Training Data**: The `data/images/` folder contains pictures of pistachios labeled with different split types. The `data/annotations/` folder has a file that tells the program which picture has which split type.
- **Model Training**: When you run the main script, it learns from the training data to understand what each split type looks like. It saves this understanding in a file.
- **Classifying New Images**: You can put new pictures of pistachios in the `new_images/` folder. Running the main script again will classify these new pictures based on what it has learned.

### Programming/File details

- **data_loader.py**:
  - `load_data()`: Reads image paths and labels from the annotation file, splits the data into training and validation sets.
  - `preprocess_image()`: Preprocesses the images for training (resizing and normalizing).
  - `create_datasets()`: Creates TensorFlow datasets for training and validation.
- **train_model.py**:
  - `build_model()`: Constructs the neural network model using MobileNetV2.
  - `train_model()`: Compiles and trains the model using the training data, applies data augmentation, and saves the trained model.
- **predict_split.py**:

  - `load_model()`: Loads the saved model.
  - `preprocess_image()`: Preprocesses new images for prediction.
  - `predict_split()`: Predicts the split type of a given image.
  - `classify_and_allocate_images()`: Classifies all images in the `new_images/` folder and moves them into corresponding subfolders based on their predicted split type.

- **main.py**: Orchestrates the entire process of loading data, training the model, and classifying new images.

## Modifying the Project

### To Use a Different Dataset

1. **Replace Images and Annotations**:

   - Put the new training images in the `data/images/` folder.
   - Update the `instances_default.json` file in `data/annotations/` with the new annotations.

2. **Delete the Existing Model**:
   - Remove `models/pistachio_model.h5` to ensure a fresh start when training the new model.

### To Change Model Architecture or Parameters

1. **Modify `train_model.py`**:
   - Adjust the `build_model()` function to change the architecture.
   - Modify the `train_model()` function to change parameters like the number of epochs, learning rate, or batch size.

### To Apply Different Data Augmentation Techniques

1. **Edit `train_model.py`**:
   - Update the `ImageDataGenerator` settings in the `train_model()` function to apply different types of data augmentation.

import os
import shutil
from PIL import Image
from collections import Counter
import csv
import statistics
from sklearn.mixture import GaussianMixture
import numpy as np


def count_pixel_colors(image_path):
    with Image.open(image_path) as img:
        pixels = list(img.getdata())
    color_count = Counter(pixels)
    return color_count


def normalize(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)


def pack_rgb_to_long(rgb_tuple):
    r, g, b = rgb_tuple
    return (r << 16) + (g << 8) + b


# Define input and output directories
input_directory = (
    r"C:\Users\smtho\Desktop\MLab\pistachio image analysis\full_nuts\processed_images"
)
output_directories = {
    "good": os.path.join(input_directory, "good"),
    "med": os.path.join(input_directory, "med"),
    "bad": os.path.join(input_directory, "bad"),
}

# Ensure output directories exist
for directory in output_directories.values():
    os.makedirs(directory, exist_ok=True)

# Iterate through all image files in the input directory
for image_file in os.listdir(input_directory):
    if image_file.endswith(".png") or image_file.endswith(
        ".jpg"
    ):  # Adjust file extensions as needed
        full_image_path = os.path.join(input_directory, image_file)

        color_count = count_pixel_colors(full_image_path)
        total_pixels = sum(color_count.values())

        # Read the normalized long values directly without writing to CSV
        normalized_long_values = [
            pack_rgb_to_long(color[:3]) for color in color_count.keys()
        ]
        normalized_long_values = [
            normalize(value, 0, 16777215) for value in normalized_long_values
        ]

        # Fit a Gaussian Mixture Model (GMM) with two components
        gmm = GaussianMixture(n_components=2)
        gmm.fit(np.array(normalized_long_values).reshape(-1, 1))

        # Get the means of the two components
        means = gmm.means_.flatten()

        # Sort the means
        sorted_means = sorted(means)

        # Find the intersection point between the two modes
        intersection_point = (sorted_means[0] + sorted_means[1]) / 2

        # Calculate percentage to the left and right of the threshold (intersection point) for this image
        left_percentage = (
            sum(value < intersection_point for value in normalized_long_values)
            / len(normalized_long_values)
            * 100
        )
        right_percentage = (
            sum(value > intersection_point for value in normalized_long_values)
            / len(normalized_long_values)
            * 100
        )

        print(f"Intersection Point for {image_file}: {intersection_point}")
        print(
            f"Percentage of values to the left of the threshold: {left_percentage:.2f}%"
        )
        print(
            f"Percentage of values to the right of the threshold: {right_percentage:.2f}%\n"
        )

        # -> Left percentage = amount of nut appearance
        # "left_percentage < x" => "small amount of shell at this percentage"
        #   x = maximum amount of shell to be 'good'
        # "left_percentage > y" => "too much shell at this percentage"
        #   y = minimum amount of shell to be 'bad'
        # Move the image to the appropriate folder based on left_percentage
        if left_percentage < 35:
            destination_folder = output_directories["good"]
        elif left_percentage > 40:
            destination_folder = output_directories["bad"]
        else:
            destination_folder = output_directories["med"]

        shutil.move(full_image_path, os.path.join(destination_folder, image_file))

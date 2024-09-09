from PIL import Image
from collections import Counter
import os
import csv


def count_pixel_colors(image_path):
    with Image.open(image_path) as img:
        pixels = list(img.getdata())
    color_count = Counter(pixels)
    return color_count


def pack_rgb_to_long(rgb_tuple):
    r, g, b = rgb_tuple
    return r * 256 * 256 + b * 256 + g  # Retrieve values of individual bytes


folder_path = (
    r"C:\Users\smtho\Desktop\MLab\pistachio image analysis\full_nuts\binary_images"
)
file_extension = ".png"

# Get a list of all .png files in the folder
png_files = [file for file in os.listdir(folder_path) if file.endswith(file_extension)]

combined_color_count = Counter()

for file_name in png_files:
    image_path = os.path.join(folder_path, file_name)
    color_count = count_pixel_colors(image_path)
    combined_color_count += color_count

# Write combined color count data to CSV file
csv_file_path = os.path.join(folder_path, "combined_color_count.csv")
with open(csv_file_path, mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(
        ["RGB", "Long Value", "Pixel Count"]
    )  # Flipped "Long Value" and "Pixel Count" here
    for color, count in combined_color_count.items():
        rgb_value = color[:3]  # Extract RGB values from the color tuple
        long_value = pack_rgb_to_long(rgb_value)
        writer.writerow([rgb_value, long_value, count])  # Flipped the order here

print(f"Combined color count data saved to: {csv_file_path}")

from PIL import Image
import os
import csv

folder_path = (
    r"C:\Users\smtho\Desktop\MLab\pistachio image analysis\full_nuts\binary_images"
)
file_extension = ".png"


def adjust_to_bw(image_path):
    with Image.open(image_path) as img:
        img = img.convert("L")  # Convert image to grayscale
        threshold = 128  # Threshold for converting grayscale to black and white
        # grayscale on a 0 to 255 (black to white) range
        img = img.point(
            lambda p: p > threshold and 255
        )  # Convert to strictly black or white
        return img


def count_pixels(img):
    width, height = img.size
    white_count = sum(1 for pixel in img.getdata() if pixel == 255)
    black_count = sum(1 for pixel in img.getdata() if pixel == 0)
    total_pixels = width * height
    white_percentage = (white_count / total_pixels) * 100
    black_percentage = (black_count / total_pixels) * 100
    return white_percentage, black_percentage


# Get a list of all .png files in the folder
png_files = [file for file in os.listdir(folder_path) if file.endswith(file_extension)]

# Calculate pixel percentages and write to CSV file
csv_file_path = os.path.join(folder_path, "pixel_percentages.csv")
with open(csv_file_path, mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["File Name", "White Pixel Percentage", "Black Pixel Percentage"])
    for file_name in png_files:
        image_path = os.path.join(folder_path, file_name)
        img = adjust_to_bw(image_path)
        white_percentage, black_percentage = count_pixels(img)
        writer.writerow(
            [file_name, f"{white_percentage:.2f}%", f"{black_percentage:.2f}%"]
        )

print(f"Pixel percentages data saved to: {csv_file_path}")

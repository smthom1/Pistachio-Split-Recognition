import os
import csv
from PIL import Image


def get_image_size(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            return width, height
    except IOError:
        print(f"Unable to open image at {image_path}")
        return None


def calculate_pixels_per_cm(image_size, ref_width_cm, ref_height_cm):
    if image_size:
        pixels_per_cm_width = image_size[0] / ref_width_cm
        pixels_per_cm_height = image_size[1] / ref_height_cm
        pixels_per_cm = (pixels_per_cm_width + pixels_per_cm_height) / 2
        return pixels_per_cm
    return None


def count_area_frequencies(source_directory, pixels_per_cm, output_csv):
    image_areas = {}  # Dictionary to store image areas and their frequencies

    for filename in os.listdir(source_directory):
        if filename.endswith(".png"):  # Changed from .jpg to .png
            image_path = os.path.join(source_directory, filename)
            img = Image.open(image_path)
            width_cm = img.width / pixels_per_cm
            height_cm = img.height / pixels_per_cm
            area_cm2 = width_cm * height_cm

            # Count image areas and their frequencies
            if area_cm2 in image_areas:
                image_areas[area_cm2] += 1
            else:
                image_areas[area_cm2] = 1

    with open(output_csv, mode="w", newline="") as csvfile:
        fieldnames = ["Area in cm²", "Frequency"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for area, frequency in image_areas.items():
            writer.writerow({"Area in cm²": area, "Frequency": frequency})

    print(f"CSV file created: {output_csv}")
    print("Area Frequencies:")
    for area, frequency in image_areas.items():
        print(f"Area: {area} cm² - Frequency: {frequency}")


def main():
    image_path = input(
        "Enter the path of the image (in .png format): "
    )  # Changed from .jpg to .png
    ref_width_cm = float(
        input("Enter the width of the reference image (centimeters): ")
    )
    ref_height_cm = float(
        input("Enter the length of the reference image (centimeters): ")
    )

    image_size = get_image_size(image_path)
    if image_size:
        pixels_per_cm = calculate_pixels_per_cm(image_size, ref_width_cm, ref_height_cm)
        if pixels_per_cm:
            print(f"Pixels per square centimeter: {pixels_per_cm:.2f}")

            source_directory = r"C:\Users\smtho\Desktop\MLab\pistachio image analysis\kernel_only\processed_images"
            output_csv = os.path.join(source_directory, "image_areas.csv")

            count_area_frequencies(source_directory, pixels_per_cm, output_csv)
        else:
            print("Failed to calculate pixels per square centimeter.")
    else:
        print("Failed to get the image size.")


if __name__ == "__main__":
    source_directory = (
        r"C:\Users\smtho\Desktop\MLab\pistachio image analysis\kernel_only"
    )
    destination_directory = r"C:\Users\smtho\Desktop\MLab\pistachio image analysis\kernel_only\processed_images"
    # process_images(source_directory, destination_directory)  # This line is commented out as it's not needed anymore
    main()


# import os
# import csv
# from PIL import Image


# def get_image_size(image_path):
#     try:
#         with Image.open(image_path) as img:
#             width, height = img.size
#             return width, height
#     except IOError:
#         print(f"Unable to open image at {image_path}")
#         return None


# def calculate_pixels_per_cm(image_size, ref_width_cm, ref_height_cm):
#     if image_size:
#         pixels_per_cm_width = image_size[0] / ref_width_cm
#         pixels_per_cm_height = image_size[1] / ref_height_cm
#         pixels_per_cm = (pixels_per_cm_width + pixels_per_cm_height) / 2
#         return pixels_per_cm
#     return None


# def make_blue_transparent(image_path):
#     try:
#         img = Image.open(image_path)
#         img = img.convert("RGBA")  # Convert to RGBA mode for transparency support
#         pixdata = img.load()

#         width, height = img.size
#         for x in range(width):
#             for y in range(height):
#                 r, g, b, a = pixdata[x, y]
#                 # Set alpha to 0 for pixels with blue component
#                 if b > r and b > g:
#                     pixdata[x, y] = (r, g, b, 0)

#         return img
#     except Exception as e:
#         print(f"Error processing image: {e}")
#         return None


# def count_area_frequencies(source_directory, pixels_per_cm, output_csv):
#     image_areas = {}  # Dictionary to store image areas and their frequencies

#     for filename in os.listdir(source_directory):
#         if filename.endswith(".png"):
#             image_path = os.path.join(source_directory, filename)
#             img = Image.open(image_path)
#             width_cm = img.width / pixels_per_cm
#             height_cm = img.height / pixels_per_cm
#             area_cm2 = width_cm * height_cm

#             # Count image areas and their frequencies
#             if area_cm2 in image_areas:
#                 image_areas[area_cm2] += 1
#             else:
#                 image_areas[area_cm2] = 1

#     with open(output_csv, mode="w", newline="") as csvfile:
#         fieldnames = ["Area in cm²", "Frequency"]
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()

#         for area, frequency in image_areas.items():
#             writer.writerow({"Area in cm²": area, "Frequency": frequency})

#     print(f"CSV file created: {output_csv}")
#     print("Area Frequencies:")
#     for area, frequency in image_areas.items():
#         print(f"Area: {area} cm² - Frequency: {frequency}")


# def process_images(source_directory, destination_directory):
#     if not os.path.exists(destination_directory):
#         os.makedirs(destination_directory)

#     for filename in os.listdir(source_directory):
#         if filename.endswith(".jpg"):
#             image_path = os.path.join(source_directory, filename)
#             processed_img = make_blue_transparent(image_path)
#             if processed_img:
#                 output_path = os.path.join(
#                     destination_directory,
#                     "transp" + os.path.splitext(filename)[0] + ".png",
#                 )
#                 processed_img.save(output_path)

#     print(f"Transparent images saved in {destination_directory}")


# def main():
#     image_path = input("Enter the path of the image (in .jpg format): ")
#     ref_width_cm = float(
#         input("Enter the width of the reference image (centimeters): ")
#     )
#     ref_height_cm = float(
#         input("Enter the length of the reference image (centimeters): ")
#     )

#     image_size = get_image_size(image_path)
#     if image_size:
#         pixels_per_cm = calculate_pixels_per_cm(image_size, ref_width_cm, ref_height_cm)
#         if pixels_per_cm:
#             print(f"Pixels per square centimeter: {pixels_per_cm:.2f}")

#             source_directory = r"C:\Users\smtho\Desktop\MLab\pistachio image analysis\kernel_only\processed_images"
#             output_csv = os.path.join(source_directory, "image_areas.csv")

#             count_area_frequencies(source_directory, pixels_per_cm, output_csv)
#         else:
#             print("Failed to calculate pixels per square centimeter.")
#     else:
#         print("Failed to get the image size.")


# if __name__ == "__main__":
#     source_directory = (
#         r"C:\Users\smtho\Desktop\MLab\pistachio image analysis\kernel_only"
#     )
#     destination_directory = r"C:\Users\smtho\Desktop\MLab\pistachio image analysis\kernel_only\processed_images"
#     process_images(source_directory, destination_directory)
#     main()

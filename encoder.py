import argparse
import numpy as np
from PIL import Image
import math
import os

DEFAULT_OUTPUT_FOLDER = "encoded_images"
IMAGE_SIZE = (1920, 1080)

def file_to_images(file_path, output_folder, image_size=IMAGE_SIZE):
    # Read the file as bytes
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    # Calculate how many pixels we need
    total_pixels = len(file_data) // 3  # 3 bytes per pixel (RGB)
    images_needed = math.ceil(total_pixels / (image_size[0] * image_size[1]))
    
    # Pad the data to fit perfectly into the images
    padded_data = file_data + b'\0' * (images_needed * image_size[0] * image_size[1] * 3 - len(file_data))
    
    # Create and save images
    for i in range(images_needed):
        start = i * image_size[0] * image_size[1] * 3
        end = start + image_size[0] * image_size[1] * 3
        img_data = np.frombuffer(padded_data[start:end], dtype=np.uint8).reshape(image_size[1], image_size[0], 3)
        img = Image.fromarray(img_data, 'RGB')
        img.save(os.path.join(output_folder, f'encoded_{i}.png'))
    
    return images_needed

def process_zip_file(file_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    num_images = file_to_images(file_path, output_folder)
    print(f"Created {num_images} images in {output_folder}")

def main():
    parser = argparse.ArgumentParser(description="Encode file to images.")
    parser.add_argument('--encode', required=True, help="File to encode.")
    parser.add_argument('--output-folder', type=str, help="Output folder for images.", default=DEFAULT_OUTPUT_FOLDER)

    args = parser.parse_args()

    process_zip_file(args.encode, args.output_folder)

if __name__ == "__main__":
    main()
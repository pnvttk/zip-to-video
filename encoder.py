import zipfile
import numpy as np
from PIL import Image
import argparse
import math
import os

DEFAULT_VIDEO_NAME = 'output.mp4'
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
PIXEL_BITS = 8  # 1 byte = 8 bits
METADATA_BITS = 32  # Bits for metadata length

def bytes_to_binary_data(byte_data):
    return ''.join(format(byte, '08b') for byte in byte_data)

def create_image_from_binary(binary_data, width, height):
    # Calculate the number of pixels we can fit in the image
    num_pixels = width * height
    
    # Ensure binary data length fits exactly in the image
    if len(binary_data) > num_pixels * PIXEL_BITS:
        raise ValueError("Binary data length exceeds the image size.")
    
    # Pad binary data to fit the image size if necessary
    binary_data = binary_data.ljust(num_pixels * PIXEL_BITS, '0')
    
    # Create a NumPy array to hold the image data
    image_array = np.zeros((height, width), dtype=np.uint8)
    
    # Fill the array with binary data
    for y in range(height):
        for x in range(width):
            # Convert binary data to grayscale pixel value
            pixel_value = int(binary_data[(y * width + x) * PIXEL_BITS:(y * width + x) * PIXEL_BITS + PIXEL_BITS], 2)
            image_array[y, x] = pixel_value
    
    # Create and return the image
    image = Image.fromarray(image_array, mode='L')  # 'L' mode for grayscale images
    return image

def process_zip_file(zip_file_path, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Read the first file in the zip (assuming one file for simplicity)
        file_name = zip_ref.namelist()[0]
        with zip_ref.open(file_name) as file:
            byte_data = file.read()
    
    binary_data = bytes_to_binary_data(byte_data)
    data_length = len(binary_data)
    
    # Add metadata to the beginning of the binary data
    metadata = format(data_length, f'0{METADATA_BITS}b')  # Metadata as binary string
    binary_data_with_metadata = metadata + binary_data
    
    # Calculate the number of images needed
    num_pixels = IMAGE_WIDTH * IMAGE_HEIGHT
    num_images = math.ceil(len(binary_data_with_metadata) / (num_pixels * PIXEL_BITS))
    
    for i in range(num_images):
        start_index = i * num_pixels * PIXEL_BITS
        end_index = min(start_index + num_pixels * PIXEL_BITS, len(binary_data_with_metadata))
        image_binary_data = binary_data_with_metadata[start_index:end_index]
        
        # Adjust the size of the image if it's the last one and doesn't fully fit
        if i == num_images - 1:
            remaining_pixels = len(image_binary_data) // PIXEL_BITS
            width = IMAGE_WIDTH
            height = math.ceil(remaining_pixels / width)
        else:
            width, height = IMAGE_WIDTH, IMAGE_HEIGHT
        
        # Create and save each image
        image = create_image_from_binary(image_binary_data, width, height)
        image_file_path = os.path.join(output_folder, f'output_image_{i + 1}.png')
        image.save(image_file_path)

def main():
    parser = argparse.ArgumentParser(description="Encode file to images.")
    parser.add_argument('--encode', required=True, help="File to encode.")
    parser.add_argument('--output-folder', type=str, help="Output folder for images.", default='output_images')

    args = parser.parse_args()

    process_zip_file(args.encode, args.output_folder)

if __name__ == "__main__":
    main()

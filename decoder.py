import numpy as np
from PIL import Image
import os
import argparse

DEFAULT_OUTPUT = 'restored_file.zip'
IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080
PIXEL_BITS = 8
METADATA_BITS = 32

def binary_data_to_bytes(binary_data):
    return bytearray(int(binary_data[i:i + 8], 2) for i in range(0, len(binary_data), 8))

def decode_image(image_path):
    image = Image.open(image_path)
    image_array = np.array(image)
    
    binary_data = ''
    for row in image_array:
        for pixel in row:
            binary_data += format(pixel, '08b')
    
    return binary_data

def process_images(output_folder):
    binary_data_with_metadata = ''
    
    for file_name in sorted(os.listdir(output_folder)):
        file_path = os.path.join(output_folder, file_name)
        binary_data_with_metadata += decode_image(file_path)
    
    # Extract metadata and binary data
    metadata = binary_data_with_metadata[:METADATA_BITS]
    data_length = int(metadata, 2)
    binary_data = binary_data_with_metadata[METADATA_BITS:METADATA_BITS + data_length]
    
    return binary_data

def main():
    parser = argparse.ArgumentParser(description="Decode images to file.")
    parser.add_argument('--decode', required=True, help="Folder containing images.")
    parser.add_argument('--output', type=str,  help="Output file name.", default=DEFAULT_OUTPUT)

    args = parser.parse_args()

    binary_data = process_images(args.decode)
    byte_data = binary_data_to_bytes(binary_data)
    
    with open(args.output, 'wb') as file:
        file.write(byte_data)

if __name__ == "__main__":
    main()

import argparse
import numpy as np
from PIL import Image
import os

DEFAULT_OUTPUT = "decoded_file.zip"

def images_to_binary_data(folder_path):
    image_files = sorted([f for f in os.listdir(folder_path) if f.startswith('encoded_') and f.endswith('.png')])
    all_data = []
    for img_file in image_files:
        img = Image.open(os.path.join(folder_path, img_file))
        img_data = np.array(img)
        all_data.extend(img_data.flatten())
    return all_data

def binary_data_to_bytes(binary_data):
    # Remove padding
    while binary_data and binary_data[-1] == 0:
        binary_data.pop()
    return bytes(binary_data)

def process_images(folder_path):
    return images_to_binary_data(folder_path)

def main():
    parser = argparse.ArgumentParser(description="Decode images to file.")
    parser.add_argument('--decode', required=True, help="Folder containing images.")
    parser.add_argument('--output', type=str, help="Output file name.", default=DEFAULT_OUTPUT)

    args = parser.parse_args()

    binary_data = process_images(args.decode)
    byte_data = binary_data_to_bytes(binary_data)
    
    with open(args.output, 'wb') as file:
        file.write(byte_data)

    print(f"File decoded and saved as {args.output}")

if __name__ == "__main__":
    main()
import os
import cv2
import math
import shutil
import argparse
import numpy as np
from PIL import Image
from utils.progressbar import tqdm

DEFAULT_OUTPUT_VIDEO = "output.avi"
DEFAULT_OUTPUT_FOLDER = "encoded_images"
IMAGE_SIZE = (1920, 1080)

def images_to_video(image_folder, output_video, fps=30.0):
    images = [img for img in os.listdir(image_folder) if img.startswith("encoded_") and img.endswith(".png")]

    # Sort images numerically
    images.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))  

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    # FFV1 codec for lossless compression
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')  
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    for image in tqdm(images, desc="Converting images to video"):
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    shutil.rmtree(image_folder, ignore_errors=True)
    print(f"Created {output_video} successfully")
    print(f"Removing {image_folder} directory")

    video.release()

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
    for i in tqdm(range(images_needed), desc="Converting file to images"):
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
    parser.add_argument('--output', type=str, help="Output video name.", default=DEFAULT_OUTPUT_VIDEO)

    args = parser.parse_args()

    process_zip_file(args.encode, DEFAULT_OUTPUT_FOLDER)
    images_to_video(DEFAULT_OUTPUT_FOLDER, args.output)

if __name__ == "__main__":
    main()
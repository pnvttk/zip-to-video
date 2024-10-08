import os
import cv2
import shutil
import argparse
import numpy as np
from PIL import Image
from utils.progressbar import tqdm

DEFAULT_OUTPUT = "restored_file.zip"
DEFAULT_INPUT_FOLDER = "decoded_images"

def video_to_images(video_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    video = cv2.VideoCapture(video_path)
    total_frame = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frame_count = 0
    with tqdm(total=total_frame, desc="Processing video frames") as pbar:
        while True:
            ret, frame = video.read()
            if not ret:
                break
            
            output_path = os.path.join(output_folder, f'decoded_{frame_count}.png')
            cv2.imwrite(output_path, frame)
            frame_count += 1
            pbar.update(1)

    video.release()
    return frame_count

def images_to_binary_data(folder_path):
    all_data = []
    image_files = sorted([f for f in os.listdir(folder_path) if f.startswith('decoded_') and f.endswith('.png')])

    for img_file in tqdm(image_files, desc="Converting images to binary data") :
        img = Image.open(os.path.join(folder_path, img_file))
        img_data = np.array(img)
        all_data.extend(img_data.flatten())

    return all_data

def binary_data_to_bytes(binary_data):
    with tqdm(total=len(binary_data), desc="Processing binary data") as pbar:
        while binary_data and binary_data[-1] == 0:
            binary_data.pop()
            pbar.update(1)  

    return bytes(binary_data)

def process_images(folder_path):
    return images_to_binary_data(folder_path)

def main():
    parser = argparse.ArgumentParser(description="Decode images to file.")
    parser.add_argument('--decode', required=True, help="Input video file.")
    parser.add_argument('--output', type=str, help="Output file name.", default=DEFAULT_OUTPUT)

    args = parser.parse_args()

    num_frames = video_to_images(args.decode, DEFAULT_INPUT_FOLDER)
    print(f"Extracted {num_frames} frames to {DEFAULT_INPUT_FOLDER}")

    binary_data = process_images(DEFAULT_INPUT_FOLDER)
    byte_data = binary_data_to_bytes(binary_data)
    
    with open(args.output, 'wb') as file:
        file.write(byte_data)

    print(f"File decoded and saved as {args.output}")
    shutil.rmtree(DEFAULT_INPUT_FOLDER, ignore_errors=True)

if __name__ == "__main__":
    main()
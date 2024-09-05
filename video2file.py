import argparse
import os
import shutil
from PIL import Image

TEMP_IMAGE_DIR = 'output_images'

def images_to_file(image_dir, output_file_path, image_size=(1920, 1080)):
    img_width, img_height = image_size
    num_pixels = img_width * img_height
    pixels = []
    
    for image_file in sorted(os.listdir(image_dir)):
        if image_file.endswith('.png'):
            img = Image.open(os.path.join(image_dir, image_file))
            img_pixels = list(img.getdata())
            
            # Print out the number of pixels read
            print(f"Pixels read from {image_file}: {len(img_pixels)}")
            
            # Limit pixels to avoid excessive data
            pixels.extend(img_pixels[:num_pixels])
    
    # Convert pixels back to bytes
    file_bytes = bytearray()
    for pixel in pixels:
        file_bytes.extend(pixel)
    
    # Check file size consistency
    if len(file_bytes) != num_pixels * 3:  # 3 bytes per pixel (RGB)
        print("Warning: Byte length does not match the expected size.")
    
    with open(output_file_path, 'wb') as file:
        file.write(file_bytes)
    
    print(f"Restored file size: {os.path.getsize(output_file_path)} bytes")

def extract_frames(video_file, output_dir, framerate=30):
    os.makedirs(output_dir, exist_ok=True)
    os.system(f'ffmpeg -i {video_file} -vf fps={framerate} {output_dir}/image_%d.png')
    
    # Print number of extracted frames
    num_frames = len([f for f in os.listdir(output_dir) if f.endswith('.png')])
    print(f"Number of frames extracted: {num_frames}")

def cleanup_images(output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print(f"Deleted temporary images directory: {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Decode video to file.")
    parser.add_argument('--decode', type=str, help="Video file to decode.")
    parser.add_argument('--output', type=str, help="File to save decoded data (optional)", default='restored_file.zip')

    args = parser.parse_args()
    
    if args.decode:
        # Extract frames from video
        extract_frames(args.decode, TEMP_IMAGE_DIR)
        
        # Convert images back to file
        images_to_file(TEMP_IMAGE_DIR, args.output)
        
        # Cleanup temporary images
        cleanup_images(TEMP_IMAGE_DIR)
        
        print(f"File saved as {args.output}")
    else:
        print("Error: --decode flag is required for decoding.")

if __name__ == "__main__":
    main()

import argparse
import os
import shutil
from PIL import Image

DEFAULT_VIDEO_NAME = 'output.mp4'
TEMP_IMAGE_DIR = 'output_images'

def file_to_images(file_path, output_dir=TEMP_IMAGE_DIR, image_size=(1920, 1080)):
    with open(file_path, 'rb') as file:
        file_bytes = file.read()
    
    os.makedirs(output_dir, exist_ok=True)
    
    img_width, img_height = image_size
    num_pixels = img_width * img_height
    pixels = [(file_bytes[i], file_bytes[i+1], file_bytes[i+2]) if i + 2 < len(file_bytes) else (0, 0, 0) for i in range(0, len(file_bytes), 3)]
    
    for i in range(0, len(pixels), num_pixels):
        img_pixels = pixels[i:i+num_pixels]
        img = Image.new('RGB', image_size)
        img.putdata(img_pixels)
        img.save(os.path.join(output_dir, f'image_{i // num_pixels}.png'))

def images_to_video(image_dir, video_file, framerate=30):
    os.system(f'ffmpeg -framerate {framerate} -i {image_dir}/image_%d.png -c:v libx264 -pix_fmt yuv420p {video_file}')

def cleanup_images(output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print(f"Deleted temporary images directory: {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Encode file to video.")
    parser.add_argument('--encode', required=True, help="File to encode.")
    parser.add_argument('--output', type=str, help="Output video file name (optional)", default=DEFAULT_VIDEO_NAME)

    args = parser.parse_args()
    
    file_to_images(args.encode)
    images_to_video(TEMP_IMAGE_DIR, args.output)
    
    # Cleanup temporary images
    cleanup_images(TEMP_IMAGE_DIR)
    
    print(f"Video saved as {args.output}")

if __name__ == "__main__":
    main()

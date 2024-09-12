# File Encoder/Decoder

This project consists of two main scripts: an encoder that converts files to a series of images and then to a video, and a decoder that reverses this process to recover the original file.

## Encoder Usage

The encoder script converts a file into a series of images, which are then compiled into a video.

```bash
python encoder.py --encode <path_to_file> [--output <output_video_name>]
```

### Arguments:
- `--encode`: (Required) Path to the file you want to encode.
- `--output`: (Optional) Name of the output video file. Default is "output.avi".

### Example:
```bash
python encoder.py --encode my_secret_file.zip --output encoded_file.avi
```

This command will:
1. Convert `my_secret_file.zip` into a series of images.
2. Compile these images into a video named `encoded_file.avi`.
3. Delete the temporary image files.

## Decoder Usage

The decoder script extracts images from a video and reconstructs the original file.

```bash
python decoder.py --decode <path_to_video> [--output <output_file_name>]
```

### Arguments:
- `--decode`: (Required) Path to the video file you want to decode.
- `--output`: (Optional) Name of the output file. Default is "restored_file.zip".

### Example:
```bash
python decoder.py --decode encoded_file.avi --output recovered_secret_file.zip
```

This command will:
1. Extract frames from `encoded_file.avi` as individual images.
2. Convert these images back into binary data.
3. Save the reconstructed file as `recovered_secret_file.zip`.
4. Delete the temporary image files.

## Notes:
- Ensure you have the required dependencies installed (`opencv-python`, `numpy`, `Pillow`).
- The encoder uses the FFV1 codec for lossless compression.
- The default image size is 1920x1080. Modify `IMAGE_SIZE` in the scripts if needed.
- Temporary files are automatically cleaned up after processing.

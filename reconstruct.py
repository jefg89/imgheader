import numpy as np
from PIL import Image
import argparse
import re

def extract_array_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Use regex to extract the array content
    match = re.search(r'const unsigned char \w+\[] = {(.*?)};', content, re.DOTALL)
    if not match:
        raise ValueError("Array data not found in the file.")

    array_str = match.group(1)
    array_str = array_str.replace('\n', '').replace(' ', '')  # Remove newlines and spaces
    array_data = array_str.split(',')

    # Convert the array data to a numpy array of uint8
    image_array = np.array([int(byte.strip(), 0) for byte in array_data if byte.strip()], dtype=np.uint8)
    return image_array

def convert_to_image(image_array, width, height, mode, mirror):
    if mode == 'binary':
        # Convert the binary array back to a flat array of 1s and 0s
        flat_array = np.unpackbits(image_array)
        # Trim the flat array to the correct size
        flat_array = flat_array[:width * height]
        # Reshape the flat array to the original dimensions
        image_data = flat_array.reshape((height, width)) * 255
    elif mode == 'grayscale':
        # Reshape the flat array to the original dimensions
        image_data = np.array(image_array).reshape((height, width))
    else:
        raise ValueError("Unsupported mode. Please use 'binary' or 'grayscale'.")

    if mirror:
        # Mirror the image horizontally
        image_data = np.fliplr(image_data)

    # Convert the NumPy array to a PIL Image
    image = Image.fromarray(image_data.astype('uint8'), 'L')
    
    return image

def main():
    parser = argparse.ArgumentParser(description='Convert an image array back to an image file.')
    parser.add_argument('output_path', type=str, help='The path to save the output image file')
    parser.add_argument('--width', type=int, required=True, help='The width of the image')
    parser.add_argument('--height', type=int, required=True, help='The height of the image')
    parser.add_argument('--mode', type=str, choices=['grayscale', 'binary'], required=True, help='The mode of the image: grayscale or binary')
    parser.add_argument('--file', type=str, required=True, help='The file containing the image array')
    parser.add_argument('--mirror', action='store_true', help='Mirror the array horizontally before converting to image')

    args = parser.parse_args()

    # Extract the array from the file
    image_array = extract_array_from_file(args.file)

    # Convert the array back to an image
    image = convert_to_image(image_array, args.width, args.height, args.mode, args.mirror)

    # Save the image
    image.save(args.output_path)
    print(f"Image saved to {args.output_path}")

if __name__ == '__main__':
    main()

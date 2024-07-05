import argparse
from PIL import Image
import numpy as np
import os

def generate_header(image_path, mode):
    # Load the image
    image = Image.open(image_path)
    
    # Convert the image to grayscale if it is not already
    if image.mode != 'L':
        image = image.convert('L')
    
    # Convert to binary if selected
    if mode == 'binary':
        threshold = 128
        image = image.point(lambda p: p > threshold and 1)
    
    image_array = np.array(image)
    width, height = image.size

    # If mode is binary, group pixels into bytes
    if mode == 'binary':
        # Flatten the array and pad with zeros to make the length a multiple of 8
        flattened = image_array.flatten()
        padding = 8 - len(flattened) % 8
        if padding != 8:
            flattened = np.pad(flattened, (0, padding), 'constant', constant_values=0)
        # Group every 8 pixels into a single byte
        binary_array = np.packbits(flattened)
        final_array = binary_array
    else:
        final_array = image_array.flatten()

    # Get the name of the image without the extension
    image_name = "IMAGE"

    # Start constructing the header content
    header_content = f"#ifndef {image_name.upper()}_H\n"
    header_content += f"#define {image_name.upper()}_H\n\n"
    header_content += f"const int {image_name}_width = {width};\n"
    header_content += f"const int {image_name}_height = {height};\n"
    header_content += f"const char* {image_name}_mode = \"{mode}\";\n"
    header_content += f"const int {image_name}_size = {len(final_array)};\n\n"

    header_content += f"const unsigned char {image_name}[] = {{\n"

    # Add the pixel values to the header content
    if mode == 'binary':
        for byte in final_array:
            header_content += f"    0x{byte:02x},\n"
    else:
        for byte in final_array:
            header_content += f"    {byte},\n"

    header_content = header_content.rstrip(",\n") + "\n};\n\n"
    header_content += f"#endif // {image_name.upper()}_H\n"

    # Write the header content to a .h file
    header_file_path = f"{image_name}.h"
    with open(header_file_path, 'w') as header_file:
        header_file.write(header_content)

    print(f"Header file '{header_file_path}' generated successfully.")

def main():
    parser = argparse.ArgumentParser(description='Generate a C/C++ header file from an image.')
    parser.add_argument('image_path', type=str, help='The full path to the image file')
    parser.add_argument('--mode', type=str, choices=['grayscale', 'binary'], default='grayscale', help='Select image mode: grayscale or binary')
    args = parser.parse_args()

    generate_header(args.image_path, args.mode)

if __name__ == '__main__':
    main()

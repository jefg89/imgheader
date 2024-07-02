import argparse
from PIL import Image
import numpy as np
import os

def generate_header(image_path):
    # Load the image
    image = Image.open(image_path)
    
    # Convert the image to grayscale if it is not already
    if image.mode != 'L':
        image = image.convert('L')
    
    image_array = np.array(image)
    width, height = image.size

    # Get the name of the image without the extension
    image_name = "IMAGE"

    # Start constructing the header content
    header_content = f"#ifndef {image_name.upper()}_H\n"
    header_content += f"#define {image_name.upper()}_H\n\n"
    header_content += f"const int {image_name}_width = {width};\n"
    header_content += f"const int {image_name}_height = {height};\n"
    header_content += f"const unsigned char {image_name}[] = {{\n"

    # Add the pixel values to the header content
    for row in image_array:
        header_content += "    " + ", ".join(map(str, row)) + ",\n"

    header_content = header_content.rstrip(",\n") + "\n};\n\n"
    header_content += f"#endif // {image_name.upper()}_H\n"

    # Write the header content to a .h file
    header_file_path = f"{image_name}.h"
    with open(header_file_path, 'w') as header_file:
        header_file.write(header_content)

    print(f"Header file '{header_file_path}' generated successfully.")

def main():
    parser = argparse.ArgumentParser(description='Generate a C/C++ header file from a grayscale image.')
    parser.add_argument('image_path', type=str, help='The full path to the image file')
    args = parser.parse_args()

    generate_header(args.image_path)

if __name__ == '__main__':
    main()

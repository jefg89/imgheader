# Image to C/C++ Header Converter

This project contains a Python script that converts a grayscale image to a C/C++ header file. The script extracts the pixel values from the image and saves them as an array in the header file, along with the image dimensions.

## Features

- Converts any image to grayscale if it's not already.
- Extracts pixel values and saves them in a C/C++ header file.
- Includes image dimensions (width and height) in the header file.

## Requirements

- Python 3.x
- Pillow (Python Imaging Library Fork)
- NumPy

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/jefg89/imgheader.git
    cd imgheader
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the script with the path to the image file as an argument:

```sh
python generate_header.py path_to_your_image.jpg

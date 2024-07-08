# -*- coding: utf-8 -*-
# @Time    : 2024/07/03 17:32
# @Author  : Kenny Zhou
# @FileName: demarcate.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

import cv2
import numpy as np
import os


def create_hls_image(h, l, s, width, height):
    """
    Create an HLS image with the given H, L, and S values.

    Parameters:
    h (int): Hue value (0-179)
    l (int): Lightness value (0-255)
    s (int): Saturation value (0-255)
    width (int): Width of the image
    height (int): Height of the image

    Returns:
    np.ndarray: HLS image
    """
    # Create an image with the specified HLS values
    hls_image = np.zeros((height, width, 3), dtype=np.uint8)
    hls_image[:] = (h, l, s)

    # Convert HLS image to BGR for display and saving
    bgr_image = cv2.cvtColor(hls_image, cv2.COLOR_HLS2BGR)
    return bgr_image


def create_grayscale_image(width, height):
    """
    Create a grayscale image with a gradient from black to white.

    Parameters:
    width (int): Width of the image
    height (int): Height of the image

    Returns:
    np.ndarray: Grayscale image
    """
    # Create a gradient from black to white
    gradient = np.linspace(0, 255, width, dtype=np.uint8)
    grayscale_image = np.tile(gradient, (height, 1))

    # Convert to 3-channel BGR image
    grayscale_image = cv2.cvtColor(grayscale_image, cv2.COLOR_GRAY2BGR)
    return grayscale_image


def ensure_directory_exists(directory):
    """
    Ensure the directory exists; if not, create it.

    Parameters:
    directory (str): Directory path to check/create
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_image(image, filename):
    """
    Save the image to a file.

    Parameters:
    image (np.ndarray): Image to save
    filename (str): Filename to save the image as
    """
    cv2.imwrite(filename, image)


def main(output_dir):
    # Ensure the output directory exists
    ensure_directory_exists(output_dir)

    # Define image dimensions
    width, height = 256, 256

    # Define HLS values to generate images
    hls_values = [
        (60, 128, 0),  #0 Red
        (60, 128, 51),  #60 Green
        (60, 128, 102),  #120 Blue
        (60, 128, 153),  #30 Yellow
        (60, 128, 204),  #90 Cyan
        (60, 128, 255)  #150 Magenta
    ]

    # Generate and save HLS images
    for i, (h, l, s) in enumerate(hls_values):
        hls_image = create_hls_image(h, l, s, width, height)
        save_image(hls_image,  os.path.join(output_dir,f'hls_{h}_{l}_{s}.png'))

    # Generate and save grayscale image
    grayscale_image = create_grayscale_image(width, height)
    save_image(grayscale_image,  os.path.join(output_dir,'grayscale.png'))


def rgb2hls(*args):
    # 定义RGB颜色值
    r,g,b = args
    rgb_color = np.uint8([[[r,g,b]]])

    # 将RGB颜色值转换为HLS
    hls_color = cv2.cvtColor(rgb_color, cv2.COLOR_RGB2HLS)

    # 输出HLS颜色值
    print("HLS颜色值:", hls_color[0][0])

if __name__ == '__main__':
    # output_dir = '/Users/kennymccormick/Pictures/Deamcate'
    # main(output_dir)
    rgb2hls(52,82,35
            )
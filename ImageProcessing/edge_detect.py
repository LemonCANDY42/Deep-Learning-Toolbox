# -*- coding: utf-8 -*-
# @Time    : 2024/06/26 10:31
# @Author  : Kenny Zhou
# @FileName: edge_detect.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_canny(image, thresholds):
    """Apply Canny edge detection with different thresholds."""
    edges = [cv2.Canny(image, t[0], t[1]) for t in thresholds]
    return edges

def apply_sobel(image, ksize_list):
    """Apply Sobel edge detection with different kernel sizes."""
    edges = [cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=k) + cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=k) for k in ksize_list]
    edges = [cv2.convertScaleAbs(e) for e in edges]
    return edges

def apply_laplacian(image, ksize_list):
    """Apply Laplacian edge detection with different kernel sizes."""
    edges = [cv2.Laplacian(image, cv2.CV_64F, ksize=k) for k in ksize_list]
    edges = [cv2.convertScaleAbs(e) for e in edges]
    return edges

def main(image_path, canny_thresholds, sobel_ksizes, laplacian_ksizes):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to open image file {image_path}")
        return

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection algorithms
    canny_edges = apply_canny(gray_image, canny_thresholds)
    sobel_edges = apply_sobel(gray_image, sobel_ksizes)
    laplacian_edges = apply_laplacian(gray_image, laplacian_ksizes)

    # Determine layout
    num_canny = len(canny_edges)
    num_sobel = len(sobel_edges)
    num_laplacian = len(laplacian_edges)
    total_images = 1 + num_canny + num_sobel + num_laplacian

    # Calculate number of rows and columns
    cols = 4  # You can adjust this value to change the number of columns
    rows = (total_images + cols - 1) // cols

    plt.figure(figsize=(20, 5 * rows))

    # Plot original image
    plt.subplot(rows, cols, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Original')
    plt.axis('off')

    # Plot Canny results
    for i, edge in enumerate(canny_edges):
        plt.subplot(rows, cols, i + 2)
        plt.imshow(edge, cmap='gray')
        plt.title(f'Canny {canny_thresholds[i]}')
        plt.axis('off')

    # Plot Sobel results
    for i, edge in enumerate(sobel_edges):
        plt.subplot(rows, cols, num_canny + i + 2)
        plt.imshow(edge, cmap='gray')
        plt.title(f'Sobel ksize={sobel_ksizes[i]}')
        plt.axis('off')

    # Plot Laplacian results
    for i, edge in enumerate(laplacian_edges):
        plt.subplot(rows, cols, num_canny + num_sobel + i + 2)
        plt.imshow(edge, cmap='gray')
        plt.title(f'Laplacian ksize={laplacian_ksizes[i]}')
        plt.axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    image_path = '/Users/kennymccormick/Pictures/PhotosExprot/IMG_2765.jpeg'  # Replace with your image path
    canny_thresholds = [(50, 150), (100, 200), (150, 250), (10, 50), (1, 10)]
    sobel_ksizes = [3, 5, 7]
    laplacian_ksizes = [1, 3, 5]

    main(image_path, canny_thresholds, sobel_ksizes, laplacian_ksizes)

# -*- coding: utf-8 -*-
# @Time    : 2024/06/26 11:28
# @Author  : Kenny Zhou
# @FileName: edge_detect_mutual.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import sys

def apply_canny(image, low_threshold, high_threshold):
    """Apply Canny edge detection."""
    return cv2.Canny(image, low_threshold, high_threshold)

def apply_sobel(image, ksize):
    """Apply Sobel edge detection."""
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=ksize)
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=ksize)
    sobel = cv2.convertScaleAbs(sobelx + sobely)
    return sobel

def apply_laplacian(image, ksize):
    """Apply Laplacian edge detection."""
    laplacian = cv2.Laplacian(image, cv2.CV_64F, ksize=ksize)
    laplacian = cv2.convertScaleAbs(laplacian)
    return laplacian

def update(val):
    """Update the edge detection results based on slider values."""
    low_threshold = canny_low_slider.val
    high_threshold = canny_high_slider.val
    sobel_ksize = int(sobel_slider.val)
    laplacian_ksize = int(laplacian_slider.val)

    canny_edges = apply_canny(gray_image, low_threshold, high_threshold)
    sobel_edges = apply_sobel(gray_image, sobel_ksize)
    laplacian_edges = apply_laplacian(gray_image, laplacian_ksize)

    ax_canny.imshow(canny_edges, cmap='gray')
    ax_sobel.imshow(sobel_edges, cmap='gray')
    ax_laplacian.imshow(laplacian_edges, cmap='gray')

    fig.canvas.draw_idle()

# Read the image
image_path = '/Users/kennymccormick/Pictures/PhotosExprot/IMG_2765.jpeg'  # Replace with your image path
image = cv2.imread(image_path)
if image is None:
    print(f"Error: Unable to open image file {image_path}")
    sys.exit()

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Create the plot
fig, ((ax_orig, ax_canny), (ax_sobel, ax_laplacian)) = plt.subplots(2, 2, figsize=(10, 10))
plt.subplots_adjust(left=0.25, bottom=0.25)

# Display the original image
ax_orig.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
ax_orig.set_title('Original')
ax_orig.axis('off')

# Initial edge detection results
canny_edges = apply_canny(gray_image, 50, 150)
sobel_edges = apply_sobel(gray_image, 3)
laplacian_edges = apply_laplacian(gray_image, 3)

# Display initial edge detection results
ax_canny.imshow(canny_edges, cmap='gray')
ax_canny.set_title('Canny')
ax_canny.axis('off')

ax_sobel.imshow(sobel_edges, cmap='gray')
ax_sobel.set_title('Sobel')
ax_sobel.axis('off')

ax_laplacian.imshow(laplacian_edges, cmap='gray')
ax_laplacian.set_title('Laplacian')
ax_laplacian.axis('off')

# Create sliders
axcolor = 'lightgoldenrodyellow'
ax_canny_low = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_canny_high = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_sobel = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
ax_laplacian = plt.axes([0.25, 0.0, 0.65, 0.03], facecolor=axcolor)

canny_low_slider = Slider(ax_canny_low, 'Canny Low', 0, 255, valinit=50, valstep=1)
canny_high_slider = Slider(ax_canny_high, 'Canny High', 0, 255, valinit=150, valstep=1)
sobel_slider = Slider(ax_sobel, 'Sobel ksize', 1, 31, valinit=3, valstep=2)
laplacian_slider = Slider(ax_laplacian, 'Laplacian ksize', 1, 31, valinit=3, valstep=2)

# Update the edge detection results when the slider values change
canny_low_slider.on_changed(update)
canny_high_slider.on_changed(update)
sobel_slider.on_changed(update)
laplacian_slider.on_changed(update)

plt.show()

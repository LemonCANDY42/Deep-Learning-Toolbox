# -*- coding: utf-8 -*-
# @Time    : 2024/07/05 10:05
# @Author  : Kenny Zhou
# @FileName: HLS_S.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

import cv2
import numpy as np

def adjust_saturation(image, increment_value):
    increment = (increment_value - 100) * 1.0 / 200
    print(increment)
    # increment = increment_value / 100.0 # -100~+100

    output_image = image.astype(np.float32) / 255.0  # 转换到0-1范围
    # 将RGB转换为HLS
    hls_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2HLS)

    # 调整饱和度
    # HLS空间中，L是亮度，S是饱和度
    if increment >= 0:
        # 增加饱和度
        alpha = 1.0 + increment  # 饱和度增加
        hls_image[:, :, 2] = hls_image[:, :, 2] * alpha  # S通道
    else:
        # 减少饱和度
        alpha = 1.0 + increment  # 饱和度减少，increment是负值
        hls_image[:, :, 2] = hls_image[:, :, 2] + (1.0 - hls_image[:, :, 2]) * alpha  # S通道

    # 修剪S通道到[0, 1]范围
    hls_image[:, :, 2] = np.clip(hls_image[:, :, 2], 0, 1)

    # 将HLS转换回BGR
    output_image = cv2.cvtColor(hls_image, cv2.COLOR_HLS2BGR) * 255.0
    output_image = np.clip(output_image, 0, 255).astype(np.uint8)

    return output_image
def on_trackbar(val):
    """
    Callback function for trackbar event.
    """
    saturation_value = cv2.getTrackbarPos('Saturation', 'Image')
    adjusted_image = adjust_saturation(src, saturation_value)
    cv2.imshow('Image', adjusted_image)

# Load the image
src = cv2.imread('/Users/kennymccormick/Pictures/PhotosExprot/IMG_4445.jpeg')

# Create a window and a trackbar
cv2.namedWindow('Image')
cv2.createTrackbar('Saturation', 'Image', 100, 200, on_trackbar)

# Initial call to adjust the saturation
on_trackbar(100)

cv2.waitKey(0)
cv2.destroyAllWindows()

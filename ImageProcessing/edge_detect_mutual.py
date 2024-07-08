# -*- coding: utf-8 -*-
# @Time    : 2024/06/26 11:28
# @Author  : Kenny Zhou
# @FileName: edge_detect_mutual.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

import cv2
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

from SmartTools.measure import timeit

# 读取图像
image = cv2.imread('/Users/kennymccormick/Pictures/PhotosExprot/IMG_2765.jpeg')
original_height, original_width = image.shape[:2]

# 调整图像大小
resize_height, resize_width = 600, 800
resized_image = cv2.resize(image, (resize_width, resize_height))
gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

# 使用Canny边缘检测
low_threshold = 100  # 提高低阈值
high_threshold = 200  # 提高高阈值
edges = cv2.Canny(gray, low_threshold, high_threshold)

# 使用形态学操作来连接断开的边缘并去除噪声
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # 更小的核
dilated = cv2.dilate(edges, kernel, iterations=1)

# 找到轮廓
contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 定义一个函数来计算轮廓的长度
def contour_length(contour):
    return cv2.arcLength(contour, True)

# 定义一个函数来过滤轮廓
def filter_contour(contour):
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    return area > 1000 and perimeter > 100

# 并行过滤轮廓
with ThreadPoolExecutor() as executor:
    filtered_contours = list(executor.map(lambda c: c if filter_contour(c) else None, contours))
    filtered_contours = [c for c in filtered_contours if c is not None]

# 找到最长的轮廓
longest_contour = max(filtered_contours, key=contour_length)
print(longest_contour)

# 创建一个空白图像来绘制最长的轮廓
mask = np.zeros_like(gray)
cv2.drawContours(mask, [longest_contour], -1, 255, thickness=cv2.FILLED)

# 使用mask来提取主要边缘
main_edges = cv2.bitwise_and(edges, edges, mask=mask)

# 定义构图线模板（例如黄金分割线）
height, width = main_edges.shape
golden_ratio = 0.618
line_position = int(width * golden_ratio)

# 找到最长轮廓的起点和终点
rect = cv2.minAreaRect(longest_contour)
box = cv2.boxPoints(rect)
box = np.int0(box)

# 计算轮廓线的角度
angle = rect[2]

# 旋转图像，使最长轮廓线与模板线对齐
center = (width // 2, height // 2)
rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated_image = cv2.warpAffine(resized_image, rotation_matrix, (width, height))

# 计算最长轮廓线在旋转后的图像中的新位置
longest_contour_2d = np.squeeze(longest_contour)
rotated_contour = cv2.transform(np.array([longest_contour_2d]), rotation_matrix)[0]

# 找到旋转后最长轮廓线的边界框
x, y, w, h = cv2.boundingRect(rotated_contour)

# 计算裁剪区域，使最长轮廓线对齐到模板线的位置
new_x = max(0, x - line_position + w // 2)
new_y = max(0, y)
new_w = min(width - new_x, w)
new_h = min(height - new_y, h)

# 计算相对于原图的裁剪区域
scale_x = original_width / resize_width
scale_y = original_height / resize_height
orig_x = int(new_x * scale_x)
orig_y = int(new_y * scale_y)
orig_w = int(new_w * scale_x)
orig_h = int(new_h * scale_y)

# 在原图上绘制准备裁剪的区域
original_with_box = image.copy()
cv2.rectangle(original_with_box, (orig_x, orig_y), (orig_x + orig_w, orig_y + orig_h), (0, 255, 0), 2)

# 在原图上绘制预定义模板线
line_x = int(orig_x + (line_position - new_x) * scale_x)
cv2.line(original_with_box, (line_x, orig_y), (line_x, orig_y + orig_h), (255, 0, 0), 2)

# 在原图上绘制最长轮廓线
scaled_longest_contour = np.int0(longest_contour * [scale_x, scale_y])
cv2.drawContours(original_with_box, [scaled_longest_contour], -1, (0, 0, 255), 2)

# 裁剪原图
cropped_original_image = image[orig_y:orig_y+orig_h, orig_x:orig_x+orig_w]

# 在裁剪后的图像上绘制预定义模板线
cv2.line(cropped_original_image, (line_x - orig_x, 0), (line_x - orig_x, orig_h), (0, 255, 0), 2)

# 显示结果
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.imshow(cv2.cvtColor(original_with_box, cv2.COLOR_BGR2RGB))
plt.title('Original Image with Box')
plt.subplot(1, 3, 2)
plt.imshow(edges, cmap='gray')
plt.title('Edges')
plt.subplot(1, 3, 3)
plt.imshow(cv2.cvtColor(cropped_original_image, cv2.COLOR_BGR2RGB))
plt.title('Cropped Image with Template Line')
plt.show()

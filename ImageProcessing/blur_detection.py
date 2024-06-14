# -*- coding: utf-8 -*-
# @Time    : 2024/06/14 17:18
# @Author  : Kenny Zhou
# @FileName: blur_detection.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

import cv2
import numpy as np

# 调整图像大小
def resize_image(image, max_width, max_height):
    """
    调整图像大小，使其适合处理并提高处理速度。
    Args:
        image (ndarray): 输入图像。
        max_width (int): 图像的最大宽度。
        max_height (int): 图像的最大高度。
    Returns:
        ndarray: 调整大小后的图像。
    """
    height, width = image.shape[:2]
    if width > max_width or height > max_height:
        aspect_ratio = width / height
        if aspect_ratio > 1:
            width = max_width
            height = int(max_width / aspect_ratio)
        else:
            height = max_height
            width = int(max_height * aspect_ratio)
        image = cv2.resize(image, (width, height))
    return image

# 计算拉普拉斯变换的方差
def variance_of_laplacian(image):
    """
    计算图像的拉普拉斯变换的方差，用于判断整体模糊程度。
    Args:
        image (ndarray): 输入灰度图像。
    Returns:
        float: 拉普拉斯变换的方差。
    """
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    return laplacian.var()

# 计算图像梯度
def compute_gradients(image):
    """
    使用Sobel算子计算图像的梯度，得到幅值和角度。
    Args:
        image (ndarray): 输入灰度图像。
    Returns:
        tuple: 幅值和角度矩阵。
    """
    grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    magnitude, angle = cv2.cartToPolar(grad_x, grad_y, angleInDegrees=True)
    return magnitude, angle

# 计算方向直方图
def compute_orientation_histogram(magnitude, angle, num_bins=8, cell_size=8):
    """
    计算图像每个小块的方向直方图。
    Args:
        magnitude (ndarray): 梯度幅值矩阵。
        angle (ndarray): 梯度角度矩阵。
        num_bins (int): 方向直方图的bin数量。
        cell_size (int): 每个小块的大小。
    Returns:
        ndarray: 方向直方图矩阵。
    """
    h, w = magnitude.shape
    bin_width = 360 / num_bins
    histogram = np.zeros((h // cell_size, w // cell_size, num_bins), dtype=np.float32)

    for i in range(0, h - cell_size, cell_size):
        for j in range(0, w - cell_size, cell_size):
            cell_mag = magnitude[i:i + cell_size, j:j + cell_size]
            cell_angle = angle[i:i + cell_size, j:j + cell_size]
            for k in range(cell_size):
                for l in range(cell_size):
                    bin_idx = int(cell_angle[k, l] / bin_width) % num_bins
                    histogram[i // cell_size, j // cell_size, bin_idx] += cell_mag[k, l]
    return histogram

# 分析方向直方图，判断是否存在运动模糊
def analyze_histogram(histogram, consistency_threshold=0.37,mean_consistency_threshold=150):
    """
    分析方向直方图，计算每个小块的方向性特征，以判断是否存在运动模糊。
    Args:
        histogram (ndarray): 方向直方图矩阵。
        threshold (float): 方向性阈值。
        consistency_threshold (float): 方向一致性阈值。
    Returns:
        bool: 如果存在运动模糊，返回True；否则返回False。
    """
    num_cells = histogram.shape[0] * histogram.shape[1]
    directionality = 0
    consistent_directions = np.zeros(histogram.shape[-1],dtype=np.float64)
    blur_hist_num = 0

    for i in range(histogram.shape[0]):
        for j in range(histogram.shape[1]):
            cell_hist = histogram[i, j]
            peak_value = np.max(cell_hist)
            total_value = np.sum(cell_hist)
            if total_value > 0:
                # 方向比性
                directionality += peak_value / total_value

            # 判断方向一致性
            if total_value > 0:
                # 最小-最大归一化到 [0, 1]
                normalized_hist = (cell_hist - cell_hist.min()) / (cell_hist.max() - cell_hist.min())
                # max_bin_idx = np.argmax(cell_hist)
                # print("normalized_hist:",normalized_hist,"consistent_directions",consistent_directions)
                consistent_directions += normalized_hist
                blur_hist_num+=1
            # else:
            #     consistency_score = 0  # 默认一致性分数，如果total_value为零

    directionality /= num_cells

    mean_consistency = np.mean(consistent_directions) / blur_hist_num
    std_consistency = np.std(consistent_directions, axis=0)
    max_consistency = np.max(consistent_directions) / blur_hist_num

    # 打印当前图片的具体数值
    print(f"Directionality: {directionality:.3f}, Max consistency: {max_consistency:.3f},mean_consistency:{mean_consistency:.3f},mean_consistency:{std_consistency}")

    # return directionality > threshold and max_consistency > consistency_threshold
    return max_consistency>consistency_threshold or mean_consistency>mean_consistency_threshold


# 主函数：处理图像并判断是否存在模糊和运动模糊
def main(image_path):
    """
    读取图像，调整大小，判断是否存在模糊和运动模糊，并输出结果。
    Args:
        image_path (str): 图像文件路径。
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("Image not found!")
        return

    resized_image = resize_image(image, 640, 480)
    laplacian_variance = variance_of_laplacian(resized_image)
    gaussian_blur_threshold = 1200.0

    print(f"Laplacian variance: {laplacian_variance:.3f}")

    if laplacian_variance < gaussian_blur_threshold:
        magnitude, angle = compute_gradients(resized_image)
        histogram = compute_orientation_histogram(magnitude, angle)
        if analyze_histogram(histogram, consistency_threshold=0.37,mean_consistency_threshold=150):
            print("Image has motion blur")
        else:
            print("Image is blurry due to Gaussian blur or other non-directional blur")
    else:
        print("Image is sharp")

if __name__ == "__main__":
    main("/Users/kennymccormick/Pictures/PhotosExprot/images.jpg")


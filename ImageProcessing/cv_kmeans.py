# -*- coding: utf-8 -*-
# @Time    : 2023/3/24 16:55
# @Author  : Kenny Zhou
# @FileName: cv_kmeans.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com
import numpy as np
import cv2

# np.random.seed(0)
#随机的二维数组，类型为np.float32
# samples = np.random.randint(0, 100, (25, 2)).astype(np.float32)
samples = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [9, 10], [10, 11], [11, 12], [12, 13], [13, 14], [14, 15], [15, 16], [16, 17], [17, 18], [18, 19], [19, 20], [20, 21], [21, 22], [22, 23], [23, 24], [24, 25], [25, 26]], dtype=np.float32)

clusterCount = 2
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
attempts = 5
flags = cv2.KMEANS_PP_CENTERS
compactness, labels, centers = cv2.kmeans(samples, clusterCount, None, criteria, attempts, flags)
print("samples: ", samples)
print("labels: ", labels)
print("centers: ", centers)
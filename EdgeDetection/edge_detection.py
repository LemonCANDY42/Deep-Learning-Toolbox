# -*- coding: utf-8 -*-
# @Time    : 2022/7/5 16:34
# @Author  : Kenny Zhou
# @FileName: edge_detection.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com
from pathlib import Path
import cv2

def edge_demo(img):
	# Scharr算子
	img = cv2.GaussianBlur(img, (7, 7), 0)
	x = cv2.Sobel(img, cv2.CV_16S, 1, 0, ksize=-1,scale=2)
	y = cv2.Sobel(img, cv2.CV_16S, 0, 1, ksize=-1)
	# ksize=-1 Scharr算子
	# cv2.convertScaleAbs(src[, dst[, alpha[, beta]]])
	# 可选参数alpha是伸缩系数，beta是加到结果上的一个值，结果返回uint类型的图像
	Scharr_absX = cv2.convertScaleAbs(x)  # convert 转换  scale 缩放
	Scharr_absY = cv2.convertScaleAbs(y)
	result = cv2.addWeighted(Scharr_absX, 0.5, Scharr_absY, 0.5, 0)
	return Scharr_absX,Scharr_absY,result
	# cv2.imshow('img', img)
	# cv2.imshow('Scharr_absX', Scharr_absX)
	# cv2.imshow('Scharr_absY', Scharr_absY)
	# cv2.imshow('result', result)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

if __name__ == "__main__":

	img = cv2.imread('/Users/kennymccormick/Documents/Work/ExtremeVision/企业微信截图_16569348941466.png',0)

	Scharr_absX,Scharr_absY,result = edge_demo(img)
	cv2.namedWindow('input_image', cv2.WINDOW_NORMAL)  # 设置为WINDOW_NORMAL可以任意缩放
	cv2.imshow('input_image', Scharr_absX)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

# -*- coding: utf-8 -*-
# @Time    : 2022/8/19 11:32
# @Author  : Kenny Zhou
# @FileName: optical_flow_demo.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

import cv2
import numpy as np

def optical_flow_instance(video_path:str):
	# The video feed is read in as
	# a VideoCapture object
	cap = cv2.VideoCapture(video_path)

	# ret = a boolean return value from
	# getting the frame, first_frame = the
	# first frame in the entire video sequence
	ret, first_frame = cap.read()

	# Converts frame to grayscale because we
	# only need the luminance channel for
	# detecting edges - less computationally
	# expensive
	prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

	# Creates an image filled with zero
	# intensities with the same dimensions
	# as the frame
	mask = np.zeros_like(first_frame)

	# Sets image saturation to maximum
	mask[..., 1] = 255

	while (cap.isOpened()):

		# ret = a boolean return value from getting
		# the frame, frame = the current frame being
		# projected in the video
		ret, frame = cap.read()

		# Opens a new window and displays the input
		# frame
		cv2.namedWindow('input', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
		cv2.imshow("input", frame)

		# Converts each frame to grayscale - we previously
		# only converted the first frame to grayscale
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# Calculates dense optical flow by Farneback method
		flow = cv2.calcOpticalFlowFarneback(prev_gray, gray,
																			 None,
																			 0.5, 3, 15, 3, 5, 1.2, 0)

		# Computes the magnitude and angle of the 2D vectors
		magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])

		# Sets image hue according to the optical flow
		# direction
		mask[..., 0] = angle * 180 / np.pi / 2

		# Sets image value according to the optical flow
		# magnitude (normalized)
		mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)

		# Converts HSV to RGB (BGR) color representation
		rgb = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)

		# Opens a new window and displays the output frame
		cv2.namedWindow('dense optical flow', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
		cv2.imshow("dense optical flow", rgb)

		# Updates previous frame
		prev_gray = gray

		# Frames are read by intervals of 1 millisecond. The
		# programs breaks out of the while loop when the
		# user presses the 'q' key
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# The following frees up resources and
	# closes all windows
	cap.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='传入视频参数.')
	# nargs='+' 获取多个参数组合为列表
	parser.add_argument('-v', type=str,metavar='file',
											help='视频路径',default="videoplayback.mp4")


	args = parser.parse_args()

	optical_flow_instance(video_path=args.v)


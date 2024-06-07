# -*- coding: utf-8 -*-
# @Time    : 2022/8/19 11:32
# @Author  : Kenny Zhou
# @FileName: optical_flow_demo.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

import cv2
import numpy as np

from pathlib import Path

def optical_flow_instance(video_path:str,save_npz:bool):
	# The video feed is read in as
	
	video_path = Path(video_path)
	# 在函数开始时创建VideoWriter对象
	save_path = str(video_path.parent) + f"/{video_path.stem}_optical_flow.mp4"
	fourcc = cv2.VideoWriter_fourcc(*"mp4v")

	# a VideoCapture object
	cap = cv2.VideoCapture(str(video_path))

	# 获取输入视频的宽度和高度&帧数
	frame_width = int(cap.get(3))  # 获取视频的宽度
	frame_height = int(cap.get(4))  # 获取视频的高度
	frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

	if save_npz:
		flow_array = np.zeros((frame_height, frame_width, 2, frame_count - 1))

	# 创建VideoWriter对象时使用获取的宽度和高度
	out = cv2.VideoWriter(save_path, fourcc, 20.0, (frame_width, frame_height))


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
	
	# save_path =str(video_path.parent) + "/optical_flow.mp4"
	# print(save_path)
		
	# video = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*"mp4v"), 20.0, (640, 480))
	i = 0
	while (cap.isOpened()):

		# ret = a boolean return value from getting
		# the frame, frame = the current frame being
		# projected in the video
		ret, frame = cap.read()
		if not ret:
			break

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
												pyr_scale=0.5, levels=3, winsize=15, iterations=3, poly_n=7, poly_sigma=1.5, flags=1) # , winsize=30,flags=0

		if save_npz:
			# Show flow vectors
			np_flow = np.array(flow)
			flow_array[:, :, :, i] = np_flow

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

		out.write(rgb)
		# Updates previous frame
		prev_gray = gray

		# video.write(rgb)

		# Frames are read by intervals of 1 millisecond. The
		# programs breaks out of the while loop when the
		# user presses the 'q' key
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		i+=1
	
	# video.release()

	# The following frees up resources and
	# closes all windows
	out.release()
	cap.release()
	cv2.destroyAllWindows()

	if save_npz:
		# 指定保存的文件名
		npz_file = str(video_path.parent) + '/flow_data.npz'
		# 保存 flow_array 到 .npz 文件
		np.savez_compressed(npz_file, flow_array=flow_array)

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='传入视频参数.')
	# nargs='+' 获取多个参数组合为列表
	parser.add_argument('-i', type=str,metavar='file',
											help='视频路径',default="videoplayback.mp4")

	parser.add_argument('-npz',help='store flow to npz,the Key is "flow_array"',action='store_true')



	args = parser.parse_args()

	optical_flow_instance(video_path=args.i,save_npz=args.npz)


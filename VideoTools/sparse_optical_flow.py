"""基于opencv的稀疏光流检测视频的运动轨迹"""

import numpy as np
import cv2

def video_optical_flow_LK(video_path):
	# 计算LK稀疏光流

	cap = cv2.VideoCapture(video_path)

	# ShiTomasi 角点检测参数
	feature_params = dict(maxCorners=100,
												qualityLevel=0.7,
												minDistance=7,
												blockSize=7)

	# lucas kanade光流法参数
	lk_params = dict(winSize=(30, 30),
									 maxLevel=3,
									 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

	# 创建随机颜色
	color = np.random.randint(0, 255, (100, 3))

	# 获取第一帧，找到角点
	ret, old_frame = cap.read()
	# 找到原始灰度图
	old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

	# 获取图像中的角点，返回到p0中
	p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

	# 创建一个蒙版用来画轨迹
	mask = np.zeros_like(old_frame)

	while (cap.isOpened()):
		ret, frame = cap.read()
		frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# 计算光流
		p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
		# 选取好的跟踪点
		good_new = p1[st == 1]
		good_old = p0[st == 1]

		# 画出轨迹
		for i, (new, old) in enumerate(zip(good_new, good_old)):
			a, b = new.ravel()
			c, d = old.ravel()
			mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
			frame = cv2.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)
		img = cv2.add(frame, mask)

		cv2.imshow('frame', img)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		# 更新上一帧的图像和追踪点
		old_gray = frame_gray.copy()

		# 获取图像中的角点，返回到p0中
		p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

		# p0 = good_new.reshape(-1, 1, 2)

	cv2.destroyAllWindows()
	cap.release()

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='传入视频参数.')
	parser.add_argument('-v', type=str,metavar='file',
											help='视频路径')

	args = parser.parse_args()
	video_optical_flow_LK(video_path=args.v)

# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 17:14
# @Author  : Kenny Zhou
# @FileName: labelVisualization.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com
from PIL import Image, ImageEnhance
import numpy as np
from pathlib import Path
import multiprocessing
from multiprocessing.pool import Pool
import argparse

# voc数据集class对应的color
def colormap(n):
	cmap = np.zeros([n, 3]).astype(np.uint8)

	for i in np.arange(n):
		r, g, b = np.zeros(3)

		for j in np.arange(8):
			r = r + (1 << (7 - j)) * ((i & (1 << (3 * j))) >> (3 * j))
			g = g + (1 << (7 - j)) * ((i & (1 << (3 * j + 1))) >> (3 * j + 1))
			b = b + (1 << (7 - j)) * ((i & (1 << (3 * j + 2))) >> (3 * j + 2))

		cmap[i, :] = np.array([r, g, b])
	return cmap

# 根据label结合colormap得到原始颜色数据
class label2image():
	def __init__(self, num_classes=21):
		self.colormap = colormap(256)[:num_classes].astype('uint8')

	def __call__(self, label):
		'''
		:param label: numpy
		:return:
		'''
		label = self.colormap[label]
		return label

def visualImg(item):
	blend = True

	path, folder_path = item

	label = Image.open(path)
	# 文件名不带后缀
	label_name = path.stem
	label_image = label2image()(label)
	label_image = Image.fromarray(label_image)

	if blend:
		# 控制输出为可视化label还是原图色彩叠加
		image = Image.open(str(path.parent)+"/"+str(path.stem)+".jpg")
		label_image = Image.blend(image, label_image, 0.5)
		label_image = ImageEnhance.Brightness(label_image).enhance(2)

	label_image.save(folder_path/Path(label_name+".png"))

def visualLabel(path,suffix="png"):

	path = Path(path)
	folder_path = path.parent/Path("Dye")
	file_list = list(path.rglob(f"*.{suffix}"))

	Path.mkdir(folder_path)

	f_ps = [folder_path] * len(file_list)
	data_item = list(zip(file_list, f_ps))

	cpu_number = multiprocessing.cpu_count()

	if len(file_list)>cpu_number:
		print(f"------------File number {len(file_list)}> cpu number {cpu_number}------------")
		pool = Pool(processes=cpu_number)
		pool.map(visualImg,data_item)
		pool.close()
		pool.join()
	else:
		for data in data_item:
			visualImg(data)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="choose the folder")
	parser.add_argument('-p', '--path', default="/Users/kennymccormick/Downloads/sample_o", type=str, help="输入路径")
	args = parser.parse_args()

	visualLabel(args.path)
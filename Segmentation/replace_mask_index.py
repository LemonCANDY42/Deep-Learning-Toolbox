# -*- coding: utf-8 -*-
# @Time    : 2022/12/2 14:26
# @Author  : Kenny Zhou
# @FileName: replace_mask_index.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com
import os, shutil
import cv2
import numpy as np
from tqdm import tqdm,trange
from PIL import Image

from pathlib import Path
import asyncio

IMGROOT = r'C:\Users\lzg\Desktop\test'  ###原始数据集的路径
SAVEROOT = r'C:\Users\lzg\Desktop\testout'  ###含有黑色烟雾的数据集的路径

async def worker(pngpaths):
	for pngname in pngpaths:
		pngpath = os.path.join(IMGROOT, pngname)
		pngfile = await Image.open(pngpath)
		maskgray = np.array(pngfile).astype(np.int32)
		if maskgray.ndim != 2:
			exit(f'{pngname} is not gray image')
		imgpath = os.path.splitext(pngpath)[0] + '.jpg'
		if cv2.imread(imgpath) is None or maskgray is None:
			print('opencv read', imgpath, 'is None')
			continue

		# num = np.any([maskgray==2, maskgray==3])
		# if num>0:
		if 2 in maskgray:
			mask = np.where([maskgray == 2] or [maskgray == 3], maskgray, 0)
			# if np.count_nonzero(mask)>0:
			maskimg = np.zeros_like(maskgray)
			pil_mask = Image.fromarray(maskimg.astype(np.uint8))
			pil_mask.save(os.path.join(SAVEROOT, pngname))
			shutil.copy(imgpath, SAVEROOT)


async def main():
	# prepare all of the paths
	if os.path.exists(SAVEROOT):
		shutil.rmtree(SAVEROOT)
	os.makedirs(SAVEROOT)
	ids_class = {0: 'background', 1: 'fire', 2: 'smoke_black', 3: 'smoke_white', 4: 'smoke_yellow'}
	pnglist = list(filter(lambda x: x.endswith('.png'), os.listdir(IMGROOT)))
	print('In', IMGROOT, 'have', len(pnglist), 'images')

	# split up the data
	chunksize = 10
	# split the operations into chunks
	tasks = list()

	for i in range(0, len(pnglist), chunksize):
		# select a chunk of filenames
		pngpaths = pnglist[i:(i + chunksize)]
		# define the task
		tasks.append(worker(pngpaths))

	for task in tqdm(asyncio.as_completed(tasks),total=len(tasks)):
		# wait for the next task to complete
		filepaths = await task

	del ids_class
	ids_class = {0: 'background', 1: 'smoke_black', 2: 'smoke_white'}
	del pnglist
	pixel_list = []
	pnglist = list(filter(lambda x: x.endswith('.png'), os.listdir(SAVEROOT)))
	for pngname in pnglist:
		pngpath = os.path.join(SAVEROOT, pngname)
		maskgray = np.array(Image.open(pngpath))
		unique_pixel = np.unique(maskgray)
		pixel_list.extend(unique_pixel.tolist())

	pixel_list = list(set(pixel_list))
	print('In', SAVEROOT, 'have pixel:')
	for x in pixel_list:
		print(ids_class[x], ':', x)

if __name__ == '__main__':
	#Run.
	asyncio.run(main())
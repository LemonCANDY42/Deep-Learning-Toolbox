# -*- coding: utf-8 -*-
# @Time    : 2023/7/6 09:49
# @Author  : Kenny Zhou
# @FileName: frame_rate_detection.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com
from PIL import Image, ImageDraw, ImageFont
import os

def pic_add_num(num, save_path):

	im01 = Image.new(mode='RGB', size=(192, 108), color=(0, 0, 0))
	foot_size = im01.width // 2
	font = ImageFont.truetype('SF-Pro.ttf', foot_size)  # 设置字体及其大小

	pos = ((im01.width - foot_size) // 1.5, (im01.height - foot_size) // 1.5)
	draw = ImageDraw.Draw(im01)
	draw.text(pos, str(num), fill=(255, 255, 255), font=font)
	# im01.show()
	im01.save(save_path + '/{}.jpg'.format(num))


if __name__ == "__main__":

	frame_rate = 25
	save_path = '/Users/kennymccormick/temp_project'
	for i in range(frame_rate+1):
		pic_add_num(i, save_path)

	os.system(f"cd {save_path}")
	output_stream = os.popen(f'ffmpeg -y -r {frame_rate} -i %d.jpg output{frame_rate}.mp4')
	output_stream.read()
	output_stream.close()
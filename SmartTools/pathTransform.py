# -*- coding: utf-8 -*-
# @Time    : 2022/7/20 14:51
# @Author  : Kenny Zhou
# @FileName: pathTransform.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

import os

def convert_path(path: str) -> str:
	return path.replace(r'\/'.replace(os.sep, ''), os.sep)

p = r"\\192.168.1.97\data\inbox\2021\12月\杨逸淳\主动式优化\done\积水识别\V6\testa"
print(convert_path(p))
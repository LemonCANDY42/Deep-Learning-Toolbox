# -*- coding: utf-8 -*-
# @Time    : 2022/11/16 22:58
# @Author  : Kenny Zhou
# @FileName: PathTools.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

import pathlib


def get_suffix_files(path:str|pathlib.Path,suffix='txt'):
	"""
	Iterate through all the files with the specified suffix in the specified folder。
	:param path:folder path
	:type path:str or Path
	:param suffix:file suffix
	:type suffix:str
	:return:files path
	:rtype:[*Path]
	"""
	p = pathlib.Path(path)

	files_path = list(p.glob(f"**/*.{suffix}"))
	return files_path

if __name__ == '__main__':
	files_path = get_suffix_files(path="/Users/kennymccormick/github/Deep-Learning-Toolbox",suffix="py")
	print(files_path)
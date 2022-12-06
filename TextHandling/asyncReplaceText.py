# -*- coding: utf-8 -*-
# @Time    : 2022/11/16 22:27
# @Author  : Kenny Zhou
# @FileName: asyncReplaceText.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

# Notice:This script will modify the file on the source file, please pay attention to the backup to avoid unnecessary damage!
# Need todo: pip install loguru
# aiofiles,atomicwrites
# load many files concurrently with asyncio in batch
# from os import listdir
# from os.path import join

import re
import asyncio
import aiofiles
from TextHandling.pathTools import get_suffix_files
from atomicwrites import atomic_write

class MatchReplace:
	__allowed = ("replace_dict",)
	def __init__(self,**kwargs):
		for k, v in kwargs.items():
			assert (k in self.__class__.__allowed)
			setattr(self, k, v)
		# self.__dict__.update(kwargs)

	def match_replace(self,match) ->str:
		value = str(match.group("value"))
		keys = list(self.replace_dict.keys())
		for k in keys:
			if k in value:
				value = value.replace(k,self.replace_dict[k])
				print(value)
				return str(match.group("start")+value+match.group("end"))

		return value 		#if value in keys else value


# load and return the contents of a list of file paths
async def load_files(filepaths,need_replace_text="",replace_text="",flag=False,start="",end="",replace_dict={}):
	"""

	:param filepaths:
	:type filepaths:
	:param need_replace_text:
	:type need_replace_text:
	:param replace_text:
	:type replace_text:
	:param flag:  Control whether to replace with conditional
	:type flag:
	:param start:
	:type start:
	:param end:
	:type end:
	:param replace_dict:
	:type replace_dict:
	:return:
	:rtype:
	"""
	# load all files
	for filepath in filepaths:
		# # open the file
		# async with aiofiles.open(filepath, 'r') as handle:
		# 	# load the contents and add to list
		# 	data = await handle.read()
		# 	# store loaded data
		# 	# data_list.append(data)
		# async with aiofiles.open(filepath, 'w') as f:
		# 	data = data.replace(need_replace_text, replace_text)
		# 	print(data)
		# 	f.write(data)
	# return (data_list, filepaths)

		# text = filepath.read_text()
		# text = text.replace(need_replace_text, replace_text)
		# filepath.write_text(text)
		mr = MatchReplace(replace_dict=replace_dict)
		async with aiofiles.open(filepath, 'r') as handle:
			text = await handle.read()
			text = text.replace(need_replace_text, replace_text)
			if flag and replace_dict:
				# print(re.findall(r"{0}(.+?){1}".format(start,end), text, re.S))
				text = re.sub(r"(?P<start>{0})(?P<value>.+?)(?P<end>{1})".format(start,end), mr.match_replace, text, re.S)
			filepath.write_text(text)

	return filepaths

# load all files in a directory into memory
async def main(path='./',need_replace_text='#$%^&',replace_text="l.w.r.f.42@gmail.com",suffix='txt',**kwargs):
	# prepare all of the paths
	paths = get_suffix_files(path,suffix=suffix)
	# split up the data
	chunksize = 10
	# split the operations into chunks
	tasks = list()
	for i in range(0, len(paths), chunksize):
		# select a chunk of filenames
		filepaths = paths[i:(i + chunksize)]
		# define the task
		tasks.append(load_files(filepaths,need_replace_text,replace_text,**kwargs))
	# execute tasks and process results as they are completed
	for task in asyncio.as_completed(tasks):
		# wait for the next task to complete
		filepaths = await task
		# process results
	# 	for filepath in filepaths:
	# 		# report progress
	# 		print(f'.loaded {filepath}')
	# print('Done')


# entry point
if __name__ == '__main__':

	def cal_cost_time(repetitions=1000):
		"""
		only for test
		:param repetitions:
		:type repetitions:
		:return:
		:rtype:
		"""
		import time
		from loguru import logger

		logger.info("Start running!")
		asyncio.run(main("/Users/kennymccormick/WorkFolder/test", need_replace_text='325AWSEDA3543146514dfd',
										 replace_text="123216311231234", suffix='txt'))
		start_time = time.time()
		for i in range(repetitions//2):
			asyncio.run(main("/Users/kennymccormick/WorkFolder/test",need_replace_text='123216311231234',replace_text="l.w.r.f.42@gmail.com",suffix='txt'))
			asyncio.run(main("/Users/kennymccormick/WorkFolder/test", need_replace_text='l.w.r.f.42@gmail.com',
											 replace_text="123216311231234", suffix='txt'))
		end_time = time.time()
		cost_time = (end_time-start_time)/repetitions*1000
		asyncio.run(main("/Users/kennymccormick/WorkFolder/test", need_replace_text='123216311231234',
										 replace_text="325AWSEDA3543146514dfd", suffix='txt'))
		logger.info("Cost time is {cost_time}ms.",cost_time=cost_time)

	# cal_cost_time()

	#Run.
	asyncio.run(main("/Users/kennymccormick/WorkFolder/测试", need_replace_text='14325AWSEDA3543146514dfdsvdsv',
									 replace_text="3543146514", suffix='xml',flag=True,start="<name>ocr</name>\n        <value>",end="</value>",replace_dict={"343":"TEST","-":"_","None":"___"}))

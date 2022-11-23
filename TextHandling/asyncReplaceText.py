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
import asyncio
# import aiofiles
from TextHandling.pathTools import get_suffix_files
from atomicwrites import atomic_write

# load and return the contents of a list of file paths
async def load_files(filepaths,need_replace_text,replace_text):
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

		text = filepath.read_text()
		text = text.replace(need_replace_text, replace_text)
		filepath.write_text(text)
	return filepaths


# load all files in a directory into memory
async def main(path='./',need_replace_text='#$%^&',replace_text="l.w.r.f.42@gmail.com",suffix='txt'):
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
		tasks.append(load_files(filepaths,need_replace_text,replace_text))
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
	import time
	from loguru import logger

	logger.info("Start running!")
	asyncio.run(main("/Users/kennymccormick/WorkFolder/test", need_replace_text='AWSEDASDFAS',
									 replace_text="123216311231234", suffix='txt'))
	repetitions = 100
	start_time = time.time()
	for i in range(repetitions//2):
		asyncio.run(main("/Users/kennymccormick/WorkFolder/test",need_replace_text='123216311231234',replace_text="l.w.r.f.42@gmail.com",suffix='txt'))
		asyncio.run(main("/Users/kennymccormick/WorkFolder/test", need_replace_text='l.w.r.f.42@gmail.com',
										 replace_text="123216311231234", suffix='txt'))
	end_time = time.time()
	cost_time = (end_time-start_time)/repetitions*1000
	asyncio.run(main("/Users/kennymccormick/WorkFolder/test", need_replace_text='123216311231234',
									 replace_text="AWSEDASDFAS", suffix='txt'))
	logger.info("Cost time is {cost_time}ms.",cost_time=cost_time)

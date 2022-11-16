# -*- coding: utf-8 -*-
# @Time    : 2022/11/16 22:27
# @Author  : Kenny Zhou
# @FileName: asyncReplaceText.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com
# Need todo: pip install aiofiles
# load many files concurrently with asyncio in batch
from os import listdir
from os.path import join
import asyncio
import aiofiles

from PathTools import get_suffix_files

# load and return the contents of a list of file paths
async def load_files(filepaths):
	# load all files
	data_list = list()
	for filepath in filepaths:
		# open the file
		async with aiofiles.open(filepath, 'r') as handle:
			# load the contents and add to list
			data = await handle.read()
			# store loaded data
			data_list.append(data)
	return (data_list, filepaths)


# load all files in a directory into memory
async def main(path='./'):
	# prepare all of the paths
	paths = get_suffix_files(path)
	# split up the data
	chunksize = 10
	# split the operations into chunks
	tasks = list()
	for i in range(0, len(paths), chunksize):
		# select a chunk of filenames
		filepaths = paths[i:(i + chunksize)]
		# define the task
		tasks.append(load_files(filepaths))
	# execute tasks and process results as they are completed
	for task in asyncio.as_completed(tasks):
		# wait for the next task to complete
		_, filepaths = await task
		# process results
		for filepath in filepaths:
			# report progress
			print(f'.loaded {filepath}')
	print('Done')


# entry point
if __name__ == '__main__':
	asyncio.run(main("/Users/kennymccormick/WorkFolder/test_path"))
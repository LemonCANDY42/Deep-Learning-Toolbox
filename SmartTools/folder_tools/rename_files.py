# -*- coding: utf-8 -*-
# @Time    : 2023/4/26 10:51
# @Author  : Kenny Zhou
# @FileName: rename_files.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

# This is a python script that can batch rename files in a folder by adding an increasing number before the original file name
# It uses pathlib module to support the file path formats of mac, windows, and linux operating systems
# It uses if "__name__" == "__main__" to run, and supports command line input to modify parameters
# Use it at your own risk and make sure to backup your files before running it

import sys
import argparse
from pathlib import Path

def batch_rename(folder, start=1):
    # Get the folder path as a Path object
    folder = Path(folder)

    # Get the list of files in the folder
    files = list(folder.iterdir())

    # Sort the files by name
    files.sort()

    # Initialize the starting number
    number = start

    # Loop through the files
    for file in files:
        # Get the file name and extension
        name = file.stem
        ext = file.suffix

        # Construct the new file name with the number before the original name
        new_name = f"{number}_{name}{ext}"

        # Construct the new file path
        new_path = folder / new_name

        # Rename the file
        file.rename(new_path)

        # Print a message
        print(f"Renamed {file} to {new_path}")

        # Increment the number
        number += 1

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Batch rename files in a folder by adding an increasing number before the original file name")

    # Add arguments for folder path and starting number
    parser.add_argument("-p", "--path",default="/Users/kennymccormick/Downloads/水体颜色可视化测试包" ,help="The folder path")
    parser.add_argument("-s", "--start", type=int, default=0, help="The starting number (default: 1)")

    # Parse the arguments
    args = parser.parse_args()

    # Check if the folder exists and is a directory
    if not Path(args.path).is_dir():
        print("Invalid folder path")
        sys.exit()

    # Call the batch rename function with the arguments
    batch_rename(args.path, args.start)

    print("Done")
# -*- coding: utf-8 -*-
# @Time    : 2024/06/07 10:55
# @Author  : Kenny Zhou
# @FileName: image_filter.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

import os
import shutil
import argparse
import importlib
from typing import List, Optional
from collections import defaultdict
from SmartTools.folder_tools.TYPES import FILE_TYPES
from PIL import Image

# Define supported image extensions
IMAGE_EXTENSIONS = FILE_TYPES["images"]

def is_image_file(file_path: str) -> bool:
    """
    Check if a file is an image based on its extension.

    :param file_path: Path to the file.
    :return: True if the file is an image, False otherwise.
    """
    return any(file_path.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)

def get_image_info(file_path: str) -> Optional[dict]:
    """
    Get information about an image file.

    :param file_path: Path to the image file.
    :return: A dictionary with image information or None if the file is not a valid image.
    """
    try:
        with Image.open(file_path) as img:
            return {
                "path": file_path,
                "width": img.width,
                "height": img.height,
                "mode": img.mode,
                "format": img.format
            }
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

def filter_images(file_list: List[str], min_width: Optional[int] = None, min_height: Optional[int] = None, channels: Optional[int] = None) -> List[str]:
    """
    Filter images based on specified criteria.

    :param file_list: List of file paths to filter.
    :param min_width: Minimum width of the image.
    :param min_height: Minimum height of the image.
    :param channels: Number of channels in the image (e.g., 3 for RGB).
    :return: List of file paths that meet the criteria.
    """
    filtered_files = []

    for file_path in file_list:
        if is_image_file(file_path):
            info = get_image_info(file_path)
            if info:
                print(info["width"],min_width,info["height"],min_height)
                if min_width and info["width"] < min_width:
                    continue
                if min_height and info["height"] < min_height:
                    continue
                if channels:
                    if channels == 3 and info["mode"] not in ["RGB", "RGBA"]:
                        continue
                    if channels == 1 and info["mode"] not in ["L", "LA"]:
                        continue
                filtered_files.append(file_path)

    return filtered_files

def main():
    parser = argparse.ArgumentParser(description="Filter images based on specified criteria.")
    parser.add_argument(
        "file_list",
        nargs="+",
        help="List of file paths to filter."
    )
    parser.add_argument(
        "--min_width",
        type=int,
        help="Minimum width of the image."
    )
    parser.add_argument(
        "--min_height",
        type=int,
        help="Minimum height of the image."
    )
    parser.add_argument(
        "--channels",
        type=int,
        choices=[1, 3],
        help="Number of channels in the image (e.g., 3 for RGB, 1 for grayscale)."
    )

    args = parser.parse_args()

    filtered_files = filter_images(
        args.file_list,
        min_width=args.min_width,
        min_height=args.min_height,
        channels=args.channels
    )

    for file in filtered_files:
        print(file)

if __name__ == "__main__":
    main()

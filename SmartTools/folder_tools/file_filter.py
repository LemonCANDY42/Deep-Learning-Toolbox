# -*- coding: utf-8 -*-
# @Time    : 2024/06/07 10:31
# @Author  : Kenny Zhou
# @FileName: file_filter.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

import os
import sys
import shutil
import argparse
import importlib
from typing import List, Optional
from collections import defaultdict
from TYPES import FILE_TYPES
import inspect
from typing import get_origin, get_args


# 动态修改 sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)
from ImageProcessing import image_filter  # 预先导入 image_filter 模块

FILTER_MODULES = {
    'image_filter': image_filter
}

def file_types_example():
    # Example usage
    for category, extensions in FILE_TYPES.items():
        print(f"{category.capitalize()} files: {', '.join(extensions)}")

def list_files(directory: str, extensions: Optional[List[str]] = None) -> List[str]:
    """
    Recursively list all files in the given directory and its subdirectories.
    Optionally filter files by their extensions. Print directory tree structure,
    total number of files, number of filtered files, and count of each extension.

    :param directory: The root directory to start the search.
    :param extensions: A list of file extensions to filter by (e.g., ['.txt', '.jpg']).
                       If None, all files are included.
    :return: A list of filtered file paths.
    """
    file_paths = []
    total_files = 0
    extension_count = defaultdict(int)

    # Normalize extensions to lowercase
    if extensions:
        extensions = [ext.lower() for ext in extensions]

    # Helper function to print directory tree (folders only)
    def print_tree(start_path: str, prefix: str = ""):
        items = [item for item in os.listdir(start_path) if os.path.isdir(os.path.join(start_path, item))]
        pointers = [("├── " if i < len(items) - 1 else "└── ") for i in range(len(items))]
        for pointer, item in zip(pointers, items):
            path = os.path.join(start_path, item)
            print(prefix + pointer + item)
            if os.path.isdir(path):
                print_tree(path, prefix + ("│   " if pointer == "├── " else "    "))

    # Collect files and count extensions
    for root, _, files in os.walk(directory):
        for file in files:
            total_files += 1
            file_path = os.path.join(root, file)
            if extensions:
                if any(file.lower().endswith(ext) for ext in extensions):
                    file_paths.append(file_path)
                    extension = os.path.splitext(file)[1].lower()
                    extension_count[extension] += 1
            else:
                file_paths.append(file_path)
                extension = os.path.splitext(file)[1].lower()
                extension_count[extension] += 1

    # Print directory tree
    print(f"{directory}'s Directory tree structure:")
    print_tree(directory)

    # Print summary
    print(f"\nTotal number of files: {total_files}")
    print(f"Number of filtered files: {len(file_paths)}")
    print("Count of each extension:")
    for ext, count in extension_count.items():
        print(f"{ext}: {count}")

    return file_paths

def move_or_copy_files(file_paths: List[str], destination: str, copy: bool = False):
    """
    Move or copy files to a new directory. If the directory exists and is not empty,
    prompt the user for confirmation. If it does not exist, create it.

    :param file_paths: List of file paths to be moved or copied.
    :param destination: The destination directory.
    :param copy: If True, copy files. If False, move files.
    """
    # Check if the destination directory exists
    if os.path.exists(destination):
        if os.listdir(destination):
            confirmation = input(f"The directory '{destination}' is not empty. Do you want to proceed? (yes/no): ")
            if confirmation.lower() != 'yes':
                print("Operation cancelled.")
                return
    else:
        os.makedirs(destination)

    # Move or copy files
    for file_path in file_paths:
        dest_path = os.path.join(destination, os.path.basename(file_path))
        if copy:
            shutil.copy2(file_path, dest_path)
            print(f"Copied: {file_path} -> {dest_path}")
        else:
            shutil.move(file_path, dest_path)
            print(f"Moved: {file_path} -> {dest_path}")


def main():
    parser = argparse.ArgumentParser(description="Move or copy files to a new directory.")
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="The root directory to start the search. Default is the current directory."
    )
    parser.add_argument(
        "--destination",
        nargs="?",
        default="./destination",
        help="The destination directory. Default is './destination'."
    )
    parser.add_argument(
        "--extensions",
        nargs="*",
        default=None,
        help="List of file extensions to filter by (e.g., .txt .jpg). Default is None (all files)."
    )
    parser.add_argument(
        "--file-type",
        choices=FILE_TYPES.keys(),
        help="Choose a file type category to filter by (e.g., images, documents)."
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy files instead of moving them. Default is to move files."
    )
    parser.add_argument(
        "--filter-module",
        choices=FILTER_MODULES.keys(),
        help="Specify an additional filter module to further filter the files."
    )

    # Parse known arguments and leave the rest for the filter module
    args, filter_args = parser.parse_known_args()

    # If file type is specified, use its extensions
    if args.file_type:
        extensions = FILE_TYPES[args.file_type]
    else:
        extensions = args.extensions

    filtered_files = list_files(args.directory, extensions)

    # If a filter module is specified, use it
    if args.filter_module:
        filter_module = FILTER_MODULES[args.filter_module]
        filter_function = getattr(filter_module, 'filter_images', None)
        if filter_function:
            # Extract allowed arguments for the filter function
            filter_function_params = inspect.signature(filter_function).parameters
            filter_function_args = {}

            # Parse filter_args to extract relevant arguments
            for i in range(0, len(filter_args)):
                arg = filter_args[i]
                print("a:",arg)
                if arg.startswith(f"--{args.filter_module}--"):
                    param_name = arg.split(f"--{args.filter_module}--")[1]
                    print(param_name,filter_function_params.keys())
                    if param_name in filter_function_params.keys():
                        filter_function_args[param_name] = filter_args[i + 1]

            print(f"filter_function_args:{filter_function_args}")
            # Convert argument values to the appropriate types
            for param_name, param in filter_function_params.items():
                if param_name in filter_function_args:
                    param_type = param.annotation
                    if param_type != inspect.Parameter.empty:
                        # Handle Optional and Union types
                        origin_type = get_origin(param_type)
                        if origin_type is not None:
                            param_type = get_args(param_type)[0]
                        print(param_name,param_type(filter_function_args[param_name]))
                        filter_function_args[param_name] = param_type(filter_function_args[param_name])


            # Call the filter function with the correct arguments
            filtered_files = filter_function(filtered_files, **filter_function_args)
        else:
            print(f"Module {args.filter_module} does not have a 'filter_images' function.")
            return

    if args.destination:
        move_or_copy_files(filtered_files, args.destination, args.copy)

if __name__ == "__main__":

    # python SmartTools/folder_tools/file_filter.py  /Users/kennymccormick/Downloads/3 --destination /Users/kennymccormick/Downloads/new  --file-type images --filter-module image_filter --image_filter--min_width 301 --image_filter--min_height 301 --image_filter--channels 3
    main()
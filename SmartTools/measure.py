# -*- coding: utf-8 -*-
# @Time    : 2024/06/27 16:53
# @Author  : Kenny Zhou
# @FileName: measure.py
# @Software: PyCharm
# @Email    ：l.w.r.f.42@gmail.com

import time
from functools import wraps

def timeit(func):
    """
    A decorator that prints the execution time of the function it decorates.

    Args:
    func (callable): The function to be measured.

    Returns:
    callable: A wrapper function that adds timing to the input function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Start timing
        result = func(*args, **kwargs)  # Call the function
        end_time = time.time()  # End timing
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result

    return wrapper
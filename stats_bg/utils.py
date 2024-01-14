from functools import wraps
from typing import Callable
import time
import logging


def timeit(func: Callable):
    """Measures any function execution time.

    Args:
        func (Callable): Function to be measured

    Returns:
        Callable: the same function with its time measured
    """
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        logging.info(f"Function {func.__name__} took {total_time:.2f} seconds")
        return result

    return timeit_wrapper

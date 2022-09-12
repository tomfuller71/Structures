import time
from itertools import chain


def time_function(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        elapsed = end - start
        unit = 's'
        if elapsed < 0.001:
            elapsed *= 1_000_000
            unit = 'ms'
        print(f"Timing: '{func.__name__}' took {elapsed:.3f}{unit} to run.")

        return result

    return wrapper


def log_function(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        args_itr = (repr(arg) for arg in args)
        kwargs_iter = (f"{key}={value}" for key,value in kwargs.items())
        func_args_str = ', '.join(chain(args_itr, kwargs_iter))
        print(f"Logging: {func.__name__}({func_args_str}) = {result}")
        
        return result

    return wrapper

def log_and_time_func(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        args_itr = (repr(arg) for arg in args)
        kwargs_iter = (f"{key}={value}" for key,value in kwargs.items())
        func_args_str = ', '.join(chain(args_itr, kwargs_iter))
        print(f"Logging: {func.__name__}({func_args_str}) = {result}")

        elapsed = end - start
        unit = 's'
        if elapsed < 0.001:
            elapsed *= 1_000_000
            unit = 'ms'
        print(f"Timing: '{func.__name__}' took {elapsed:.3f}{unit} to run.")
            
        return result

    return wrapper


def main():
    # chained wrapping results in the function running in effect twice
    # @time_function
    # @log_function
    @log_and_time_func
    def multiply_values(*values, round=False):
        product = 1
        for value in values:
            product *= value
        return product

    multiply_values(1, 2, 3, 4, round=True)

if __name__ == "__main__":
    main()

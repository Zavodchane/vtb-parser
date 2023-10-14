import time


def timer(func):
    def _wrapper(*args, **kwargs):
        s_t = time.time()
        result = func(*args, **kwargs)
        e_t = time.time()
        print(f"Время работы '{func.__name__}()': {e_t - s_t}")
        return result
    return _wrapper

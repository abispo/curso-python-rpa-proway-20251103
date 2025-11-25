from functools import wraps
import time

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        print(f"{func.__name__} foi executada em {end_time-start_time}")

        return result
    return wrapper

def check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) < 3:
            raise Exception("Essa função precisa ter pelo menos 3 parâmetros")
        result = func(*args, **kwargs)
        return result
    return wrapper

@timer
def task(delay):
    time.sleep(delay)

@check
def ola():
    print("Ola")

if __name__ == "__main__":

    task(2)
    task(5)
    task(1.5)
    ola()
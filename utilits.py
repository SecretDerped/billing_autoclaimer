import logging
import time

console_out = logging.StreamHandler()
file_log = logging.FileHandler("application.log", mode="w")
logging.basicConfig(handlers=(file_log, console_out), level=logging.INFO,
                    format='[%(asctime)s | %(levelname)s]: %(message)s')


def log_print(func):
    def _wrapper(*args, **kwargs):
        logging.info(f'Call - {func.__name__}{args} {kwargs}')
        start_time = time.time()
        result = func(*args, **kwargs)
        exec_time = time.time() - start_time
        logging.info(f'Result ({exec_time:.3f} sec.) - {func.__name__}{args} {kwargs}: {result}')
        return result
    return _wrapper


if __name__ == '__main__':
    pass

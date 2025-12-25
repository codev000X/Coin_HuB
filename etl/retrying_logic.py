import time
from logging import get_logger
from functools import wraps

# Use your global logger or configure one
logger = get_logger("load")  

def retry(max_retries=3, delay=1, exceptions=(Exception,)):
    """
    Retry decorator for any function that might fail.
    
    Args:
        max_retries (int): How many times to attempt before giving up.
        delay (int | float): Seconds to wait between retries.
        exceptions (tuple): Exceptions that trigger a retry.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_retries:
                try:
                    result = func(*args, **kwargs)
                    logger.info(f"{func.__name__} succeeded on attempt {attempt+1}")
                    return result
                except exceptions as e:
                    attempt += 1
                    if attempt < max_retries:
                        logger.warning(
                            f"{func.__name__} failed on attempt {attempt}: {e}. Retrying in {delay}s..."
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"{func.__name__} failed after {max_retries} attempts: {e}"
                        )
                        raise
        return wrapper
    return decorator

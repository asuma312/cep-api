import logging
from flask import request
from functools import wraps

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
request_logger = logging.getLogger("request_logger")
db_logger = logging.getLogger("db_logger")

def log_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request_logger.info(f"Endpoint accessed: {request.path}")
        request_logger.info(f"Request method: {request.method}")
        request_logger.info(f"Request data: {request.get_json() if request.method in ['POST', 'PUT'] else request.args}")
        return func(*args, **kwargs)
    return wrapper

def log_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            request_logger.error(f"Error occurred: {str(e)}")
            raise
    return wrapper

def log_db_operation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            db_logger.info(f"Database operation: {func.__name__}, Args: {args}, Kwargs: {kwargs}")
            return result
        except Exception as e:
            db_logger.error(f"Database error: {func.__name__}, Error: {str(e)}")
            raise
    return wrapper

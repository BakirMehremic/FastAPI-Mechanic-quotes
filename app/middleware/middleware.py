from fastapi import Request
from core.logger import logger
import time


async def log_middleware(request: Request, call_next):
    started = time.time()

    response = await call_next(request)

    ended = time.time()-started 

    response_status = response.status_code

    log_dict = {
        "url": request.url.path,
        "method": request.method,
        "time_taken": round(ended, 4),
        "response status": response_status
    }

    warning_statuses = [409, 406]
    error_statuses = [404, 401]
    critical_statuses = [500, 501]

    if response_status in warning_statuses:
        logger.warning(log_dict)
    elif response_status in error_statuses:
        logger.error(log_dict)
    elif response_status in critical_statuses:
        logger.critical(log_dict)
    else:
        logger.info(log_dict)

    return response

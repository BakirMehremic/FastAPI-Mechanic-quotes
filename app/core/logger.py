import logging 
import sys 

logger = logging.getLogger()


# defining the output format
formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s"
    #time of log    level of log    message passed to logger
)


# creating andlers for console and file
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler(".././logs.log")


# setting output format
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# adding handlers to the logger
logger.handlers = [stream_handler, file_handler]


# setting the default logger level
logger.setLevel(logging.INFO)
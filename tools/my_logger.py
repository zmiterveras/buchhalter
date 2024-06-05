import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # datefmt='%d-%b-%Y %H:%M:%S"
# logging.basicConfig(level=logging.DEBUG, format=FORMAT)
my_formatter = logging.Formatter(FORMAT, datefmt='%d-%b-%Y %H:%M:%S')
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(my_formatter)
logger.addHandler(stream_handler)



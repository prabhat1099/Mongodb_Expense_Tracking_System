import logging 

# create custom logger
def setup_logger(name, level =logging.DEBUG , file_name = "db_server.log"):
    logger = logging.getLogger(name)
    logger.setLevel(level= level)

    # Create file for logging
    file_handler = logging.FileHandler(file_name)
    formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(name)s-%(message)s')

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
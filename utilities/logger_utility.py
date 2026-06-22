import logging


def _logger(name):

    #Initialize Logger:
    logger = logging.getLogger(name)

    #Set Logger Level:
    logger.setLevel(logging.DEBUG)

    #Create Streamhandler
    stream_handler = logging.StreamHandler()

    #Create Formatter
    base_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    #Assign Formatter to Handler.
    stream_handler.setFormatter(base_formatter)

    #Set Handlers Level
    stream_handler.setLevel(logging.DEBUG)

    # Add Handler to Logger instance.
    logger.addHandler(stream_handler)

    #Finally, return logger.
    return logger
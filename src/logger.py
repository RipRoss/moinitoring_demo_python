import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(process)d:%(thread)d] %(filename)s:%(lineno)d - %(message)s',
    handlers=[
        logging.StreamHandler()  # log to the console
    ]
)
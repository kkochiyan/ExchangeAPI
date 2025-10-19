import sys
from loguru import logger

def setup_logger():
    logger.remove()

    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True,
        backtrace=True,
        diagnose=True
    )

    logger.add(
        "logs/app_{time}.json",
        format="{message}",
        level="DEBUG",
        rotation="10 MB",
        retention="30 days",
        serialize=True,
        compression="zip",
        backtrace=True,
        diagnose=True
    )

    return logger

my_logger = setup_logger()
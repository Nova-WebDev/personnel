import logging

logger = logging.getLogger("voucher_service")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

handler.setFormatter(formatter)
logger.addHandler(handler)

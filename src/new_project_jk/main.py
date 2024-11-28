from utils.logger import get_logger
logger = get_logger(__name__)

if __name__ == "__main__":
    logger.debug("デバッグ情報")
    logger.info("通常の情報")
    logger.warning("警告")
    logger.error("エラー")

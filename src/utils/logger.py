import logging
from pathlib import Path


# ログ設定
class LOG:
    FILE = 'logs/app.log'
    FORMAT = '[%(asctime)s.%(msecs)03d][%(levelname)s][%(pathname)s] %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    ENCODING = 'utf-8'


def get_logger(name: str = __name__) -> logging.Logger:
    """カスタマイズされたロガーインスタンスを生成する

    Args:
        name (str, optional): ロガー名。通常はモジュール名（__name__）を使用。デフォルトは__name__。

    Returns:
        logging.Logger: 設定済みのロガーインスタンス。
            - ファイル出力: すべてのログレベルをlogs/app.logに出力
            - コンソール出力: INFOレベル以上を出力
            - フォーマット: [時刻][ログレベル][ファイルパス] メッセージ
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # 共通のフォーマット設定
        formatter = logging.Formatter(LOG.FORMAT, LOG.DATE_FORMAT)

        # ファイル出力（全レベル）
        fh = logging.FileHandler(Path(LOG.FILE), encoding=LOG.ENCODING)
        fh.setFormatter(formatter)

        # コンソール出力（INFO以上）
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        # プロパゲーションを防ぐ
        logger.propagate = False

    return logger

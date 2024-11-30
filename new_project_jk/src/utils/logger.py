import logging

from config.settings import LOG_FORMAT, LOG_DATE_FORMAT, LOG_FILE, ENCODING


def get_logger(name: str = __name__) -> logging.Logger:
    """カスタマイズされたロガーインスタンスを生成する

    Args:
        name (str, optional): ロガー名。通常はモジュール名（__name__）を使用。デフォルトは__name__。

    Returns:
        logging.Logger: 設定済みのロガーインスタンス。
            - ファイル出力: すべてのログレベルをlogs/app.logに出力
            - コンソール出力: INFOレベル以上を出力
            - フォーマット: [時刻] [ログレベル] メッセージ [ファイルパス]
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 共通のフォーマット設定
    formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)

    # ファイル出力（全レベル）
    fh = logging.FileHandler(LOG_FILE, encoding=ENCODING)
    fh.setFormatter(formatter)

    # コンソール出力（INFO以上）
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

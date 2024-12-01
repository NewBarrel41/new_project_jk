import logging
from pathlib import Path
from config.settings import LOG_FILE, LOG_TEST_FILE, LOG_FORMAT, LOG_DATE_FORMAT, ENCODING


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

    # ファイル出力先の決定（'test'が含まれていればテストログへ）
    logfile = Path(LOG_TEST_FILE if 'test_' in name else LOG_FILE)

    if not logger.handlers:
        # 共通のフォーマット設定
        formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)

        # ファイル出力（全レベル）
        fh = logging.FileHandler(logfile, encoding=ENCODING)
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

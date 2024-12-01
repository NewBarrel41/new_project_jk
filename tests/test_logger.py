import pytest
from os import SEEK_END, SEEK_CUR
import logging
from utils.logger import get_logger
from config.settings import LOG_FILE, LOG_TEST_FILE, ENCODING


@pytest.fixture(autouse=True)
def reset_logging():
    """テスト前にロギングをリセット"""
    print()
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    print('loggers', loggers)
    for logger in loggers:
        print(f"Clearing handlers for logger: {logger.name}")
        print(f"Had handlers: {logger.handlers}")
        logger.handlers.clear()


@pytest.mark.parametrize('logger_name, expected_logfile', [(get_logger.__name__, LOG_FILE), (__name__, LOG_TEST_FILE)])
def test_logger_output(logger_name, expected_logfile):
    """ロガー名に応じて適切なログファイルに出力されることをテスト"""
    logger = get_logger(logger_name)
    message = f'Message from {logger_name}'
    logger.info('Start test_logger_output')
    for levelname in ['debug', 'info', 'warning', 'error']:
        getattr(logger, levelname)(message)
        with open(expected_logfile, 'rb') as f:
            # ファイルの終わりから2バイト前に移動し、改行文字が見つかるまで逆方向に読み進める
            f.seek(-2, SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, SEEK_CUR)

            # 最終行を読み込み、デコードして文字列として返す
            last_line = f.readline().decode(ENCODING)
            assert message in last_line

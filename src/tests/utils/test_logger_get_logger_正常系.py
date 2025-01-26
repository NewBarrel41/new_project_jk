import pytest
import logging
from freezegun import freeze_time
from types import SimpleNamespace as sns

from utils.logger import LOG, get_logger


def simple_with_oepn(path, mode, encoding='utf-8'):
    # ファイル読み込みと書き出しのみ
    if 'r' in mode:
        with open(path, mode, encoding=encoding) as f:
            return f.read()
    elif 'w' in mode:
        with open(path, mode, encoding=encoding) as f:
            return f.write()


@pytest.fixture(autouse=True)
def reset_logging():
    # テスト前にロギングをリセット
    print()
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.handlers.clear()
    logging.getLogger().handlers.clear()


timestamp = '2025-01-25 18:00:00.000'
params = {
    '1:ロガーのテスト': (
        sns(name=__name__),
        sns(
            level='info',
            message='Test Message.',
            test_log_file=r'logs\app_test.log',
            file=__file__.replace('C:', 'c:')
        ),
        sns(output=None)
    ),
}


@freeze_time(f'{timestamp}+0900')
@pytest.mark.parametrize('_input, _mock, _output', list(params.values()), ids=list(params.keys()))
def test_get_logger_output(caplog, mocker, _input, _mock, _output):
    # モック
    mocker.patch.object(LOG, 'FILE', _mock.test_log_file)  # クラス変数の場合はreturn_valueは要らない
    mocker.Mock(spec=logging)

    # テストコード実行
    logger = get_logger(_input.name)
    getattr(logger, _mock.level)(_mock.message)

    # アサート
    test_log = simple_with_oepn(_mock.test_log_file, 'r')
    test_log = test_log.split('\n')[-2]
    expected_log = f'[{timestamp}][{_mock.level.upper()}][{_mock.file}] {_mock.message}'
    assert test_log == expected_log  # ログが想定通りか確認
    assert logger == get_logger(_input.name)  # 同じ__name__で呼ばれたときに同じハンドラを返すか確認

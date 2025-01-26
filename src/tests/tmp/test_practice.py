import pytest
import httpx
import asyncio
from types import SimpleNamespace as sns

from tmp.practice import CallAPI


@pytest.fixture(autouse=True)
def reset_logging():
    print()


main_params = {
    '1:mainメソッドのテスト': (
        sns(input=''),
        sns(return_value=['OK1', 'OK2', 'OK3']),
        sns(
            expected_result=['OK1', 'OK2', 'OK3'],
            expected_main_args=[('new_project_jk', '1'), ('new_project_jk', '2'), ('new_project_jk', '3')]
        )
    ),
}


@pytest.mark.parametrize('_input, _mock, _output', list(main_params.values()), ids=list(main_params.keys()))
def test_main(mocker, _input, _mock, _output):
    api = CallAPI()

    # モック
    mock_async_main = mocker.AsyncMock(return_value=_mock.return_value)
    api._main = mock_async_main
    mock_asyncio_run = mocker.Mock(return_value=_mock.return_value)
    mocker.patch.object(asyncio, 'run', mock_asyncio_run)
    # mocker.patch.object(asyncio, 'run', return_value=_mock.return_value)

    # テスト実行
    result = api.main()

    # アサート
    assert result == _output.expected_result
    assert list(mock_async_main.call_args.args[0]) == _output.expected_main_args  # 引数のチェック
    # assert_called_once(): 引数をチェックせずに1回だけ呼び出されたことを確認
    # assert_called_with(): 呼び出し回数を考慮せず最後の呼び出しの引数を確認
    # assert_has_calls(): 複数回の呼び出しや順序を確認


async_main_params = {
    '1:_mainメソッドのテスト': (
        sns(ec=[('new_project_jk', '1'), ('new_project_jk', '2'), ('new_project_jk', '3')]),
        sns(call_response=['OK1', 'OK2', 'OK3']),
        sns(expected=['OK1', 'OK2', 'OK3'])
    ),
}


@pytest.mark.asyncio
@pytest.mark.parametrize('_input, _mock, _output', list(async_main_params.values()), ids=list(async_main_params.keys()))
async def test_async_main(mocker, _input, _mock, _output):
    api = CallAPI()

    # モック
    mock_async_call = mocker.AsyncMock(side_effect=_mock.call_response)
    api._call = mock_async_call
    mock_client = mocker.AsyncMock()
    mocker.patch.object(httpx, 'AsyncClient', return_value=mock_client)
    mock_asyncio_gather = mocker.AsyncMock(return_value=_mock.call_response)
    mocker.patch.object(asyncio, 'gather', mock_asyncio_gather)  # return_valueは使わない

    # テスト実行
    result = await api._main(_input.ec)

    # アサート
    assert result == _output.expected
    mock_asyncio_gather.assert_called_once()
    assert mock_async_call.call_count == len(_output.expected)
    mock_client.__aenter__.assert_called_once()
    mock_client.__aexit__.assert_called_once()


acync_call_params = {
    '1:_callメソッドのテスト': (
        sns(
            end='new_project_jk',
            cid='1'
        ),
        sns(reason_phrase='テストOK'),
        sns(expected='テストOK1')
    ),
}


@pytest.mark.asyncio
@pytest.mark.parametrize('_input, _mock, _output', list(acync_call_params.values()), ids=list(acync_call_params.keys()))
async def test_acync_call(mocker, _input, _mock, _output):
    # httpxのセッションをモック
    mock_session = mocker.AsyncMock()
    mock_session.get.return_value.reason_phrase = _mock.reason_phrase

    # テスト実行
    api = CallAPI()
    result = await api._call(mock_session, api.base_url+_input.end, _input.cid)

    # アサート
    assert result == _output.expected

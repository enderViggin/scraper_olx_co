import pytest
import pytest_mock
from ax.result.storage import Storage


class TestStorage:

    @pytest.mark.asyncio
    async def test_storage_init(self, mocker: pytest_mock.MockFixture):
        minio_mock = mocker.patch('ax.result.storage.Minio')
        storage = Storage('demo')
        minio_mock.assert_called_once_with('minio.rexuni.com', access_key='AKIAIOSFJKHSSKJHSUIY',
                                           secret_key='sjhshjhGHJGJGsg/SGHJ767/JKHKJHAJKHKAH', secure=True)

    @pytest.mark.asyncio
    async def test_storage_put(self, mocker: pytest_mock.MockFixture):
        storage = Storage('demo')
        put_object_mock = mocker.patch.object(storage.client, 'put_object', autospec=True)

        storage.put('object', b'some_data')

        call = put_object_mock.call_args_list[0]
        assert call.args[0] == 'demo'
        assert call.args[1] == 'object'
        assert call.args[2].read() == b'some_data'
        assert call.args[3] == 9
        assert call.args[4] == None

    @pytest.mark.asyncio
    async def test_storage_get(self, mocker: pytest_mock.MockFixture):
        storage = Storage('demo')
        get_object_mock = mocker.patch.object(storage.client, 'get_object', autospec=True)

        storage.get('object')

        call = get_object_mock.call_args_list[0]
        assert call.args[0] == 'demo'
        assert call.args[1] == 'object'

#TODO: Test errors
import logging

import pytest
import ax.processor
import logging
import pytest
import pytest_mock

SAVER_URL = 'https://saver-api.goscraping.com'


class TestProcessor:

    @pytest.mark.asyncio
    async def test_processor_create(self):
        app, processor = ax.processor.AppProcessor(SAVER_URL)

        # TODO: Check processor class called

        assert type(app) == ax.processor.Celery
        assert type(processor) == ax.processor.Processor
        assert processor.saver_url == SAVER_URL

        # TODO: RabbitMQ to config?
        assert app.conf.broker_url == 'amqp://dan:AUgNMVnwFuGE4Xg3@node1.rexuni.com//'
        assert app.conf.result_backend == f'backend:APIBackend://{SAVER_URL}'

    @pytest.mark.asyncio
    async def test_processor_task_wrap(self, mocker: pytest_mock.MockFixture):
        app, processor = ax.processor.AppProcessor(SAVER_URL)
        stub = mocker.stub(name='task executed')

        # send_mock = mocker.patch.object(processor, 'test', autospec=True)

        @processor.task()
        def test_task(self, **kwargs):
            stub()
            assert self.processor == processor, 'incorrect processor'
            assert str(type(self)) == "<class 'ax.processor._inner'>", 'wrong type of task'
            assert str(type(self.request)) == "<class 'celery.app.task.Context'>", 'wrong type of request'

            assert self.request.save_to is None, 'save_to not empty'

            # self.send('hello')
            return {'result': 42}

        result = test_task()

        stub.assert_called_once(), 'handler was not called'
        # send_mock.assert_called_once_with('hello'), 'apply_result called'
        assert result == {'result': 42}

    @pytest.mark.asyncio
    async def test_task_params_decorator(self, mocker: pytest_mock.MockFixture):
        app, processor = ax.processor.AppProcessor(SAVER_URL)
        stub = mocker.stub(name='task executed')

        @processor.task(save_to='some_queue')
        def test_task(self, **kwargs):
            stub()
            assert self.request.save_to is 'some_queue', 'incorrect save_to param'

        test_task()
        stub.assert_called_once(), 'handler was not called'

    @pytest.mark.asyncio
    async def test_task_params(self, mocker: pytest_mock.MockFixture):
        app, processor = ax.processor.AppProcessor(SAVER_URL)
        stub = mocker.stub(name='task executed')

        @processor.task()
        def test_task(self, **kwargs):
            stub()
            assert self.request.save_to is 'task', 'incorrect save_to param'

        test_task(save_to='task')
        stub.assert_called_once(), 'handler was not called'

    @pytest.mark.asyncio
    async def test_task_params_priority(self, mocker: pytest_mock.MockFixture):
        app, processor = ax.processor.AppProcessor(SAVER_URL)
        stub = mocker.stub(name='task executed')

        @processor.task(save_to='decorator')
        def test_task(self, **kwargs):
            stub()
            logging.error(f'{self.request=}')
            send_mock = mocker.patch.object(self, 'apply_async', autospec=True)

            assert self.request.save_to is 'task', 'incorrect save_to param'
            self.new_task(url='123')

            # send_mock.assert_called_once_with('hello'), 'apply_result called'

        test_task(save_to='task')
        stub.assert_called_once(), 'handler was not called'

# create related task from task
# keep same queue
# keep save save_to if overriden

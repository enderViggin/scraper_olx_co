import requests
from celery.backends.base import KeyValueStoreBackend
import celery
import requests
from kombu.utils.encoding import bytes_to_str, ensure_bytes
from celery import current_app, group, maybe_signature, states
import redis
import ujson
from celery.exceptions import (BackendGetMetaError, BackendStoreError,
                               ChordError, ImproperlyConfigured,
                               NotRegistered, SecurityError, TaskRevokedError,
                               TimeoutError)
from celery.utils.serialization import (create_exception_cls,
                                        ensure_serializable,
                                        get_pickleable_exception,
                                        get_pickled_exception,
                                        raise_with_context)
from celery.utils.time import get_exponential_backoff_interval
r = redis.Redis(host='localhost', port=6379, db=0)


class APIBackend(KeyValueStoreBackend):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = kwargs['url'].replace('backend:APIBackend://', '')
        self.app = kwargs['app']

    def store_result(self, task_id, result, state,
                     traceback=None, request=None, **kwargs):
        """Update task state and result.

        if always_retry_backend_operation is activated, in the event of a recoverable exception,
        then retry operation with an exponential backoff until a limit has been reached.
        """
        # print(f'store results {result=}, {state=}, {request=}')
        result = self.encode_result(result, state)

        retries = 0
        while True:
            try:
                self._store_result(task_id, result, state, traceback,
                                   request=request, **kwargs)
                return result
            except Exception as exc:
                if self.always_retry and self.exception_safe_to_retry(exc):
                    if retries < self.max_retries:
                        retries += 1

                        # get_exponential_backoff_interval computes integers
                        # and time.sleep accept floats for sub second sleep
                        sleep_amount = get_exponential_backoff_interval(
                            self.base_sleep_between_retries_ms, retries,
                            self.max_sleep_between_retries_ms, True) / 1000
                        self._sleep(sleep_amount)
                    else:
                        raise_with_context(
                            BackendStoreError("failed to store result on the backend", task_id=task_id, state=state),
                        )
                else:
                    raise

    def _store_result(self, task_id, result, state,
                      traceback=None, request=None, **kwargs):
        meta = self._get_result_meta(result=result, state=state,
                                     traceback=traceback, request=request)
        meta['task_id'] = bytes_to_str(task_id)

        if hasattr(request, 'save_to'):
            meta['save_to'] = request.save_to

        if hasattr(request, 'unfold'):
            meta['unfold'] = request.unfold


        # Retrieve metadata from the backend, if the status
        # is a success then we ignore any following update to the state.
        # This solves a task deduplication issue because of network
        # partitioning or lost workers. This issue involved a race condition
        # making a lost task overwrite the last successful result in the
        # result backend.
        # TODO: Get meta only?
        # current_meta = self._get_task_meta_for(task_id)
        #
        # if current_meta['status'] == states.SUCCESS:
        #     return result

        try:
            self._set_with_state(self.get_key_for_task(task_id), self.encode(meta), state)
        except BackendStoreError as ex:
            raise BackendStoreError(str(ex), state=state, task_id=task_id) from ex

        return result

    def get(self, key):
        # print(f'get {key}')
        # print(f'{self.endpoint}/task/{key.decode()}')
        r = requests.get(f'{self.endpoint}/task/{key.decode()}', headers={})
        return r.text

    def set(self, key, value):
        print(f'set {key} - {value} - {type(value)}')



        # r = requests.post(f'{self.endpoint}/task/{key.decode()}', json=ujson.loads(value), headers={})
        # return r.json()

    def mget(self, keys):
        for key in keys:
            yield self.get(key)

    def delete(self, key):
        print(f'delete {key}')
        r.delete(key)
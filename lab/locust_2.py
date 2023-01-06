"""
    THIS FILE IS EXPERIME

"""

import grpc
from locust import events, HttpUser, task
from locust.exception import LocustError
from locust.user.task import LOCUST_STATE_STOPPING
import gevent
import time


# patch grpc so that it uses gevent instead of asyncio
import grpc.experimental.gevent as grpc_gevent
from typing import Any, Callable

grpc_gevent.init_gevent()


class GrpcClient:
    def __init__(self, stub):
        self._stub_class = stub.__class__
        self._stub = stub

    def __getattr__(self, name):
        func = self._stub_class.__getattribute__(self._stub, name)

        def wrapper( *args, **kwargs):
            method=Callable
            response = None
            exception = None
            response_length = 0

            start_time = time.perf_counter()
            try:
                response = func( *args, **kwargs)
                # response = method(*args, **kwargs)
                # if isinstance(response, Employee)
                try:
                    response_length = len(list(response))
                except:
                    pass
                try:
                    response_length = response.message
                except:
                    pass
            
            except grpc.RpcError as e:
                exception = e

            request_meta = {
                "request_type": "grpc",
                "name": self._stub,
                "response_time":(time.perf_counter() - start_time) * 1000,
                "response_length": response_length,
                "exception": exception,
                "context": None,
                "response": response,
            }

            events.request.fire(**request_meta)
            return request_meta["response"]

        return wrapper


class GrpcUser(HttpUser):
    abstract = True
    vacancy_service_stub_class = None
    auth_service_stub_class = None


    def __init__(self, environment):
        super().__init__(environment)
        for attr_value, attr_name in ((self.host, "host"), (self.vacancy_service_stub_class, "vacancy_service_stub_class"),  (self.auth_service_stub_class, "auth_service_stub_class")):
            if attr_value is None:
                raise LocustError(f"You must specify the {attr_name}.")

        self._channel = grpc.insecure_channel(self.host)
        self._channel_closed = False
        vacancy_service_stub = self.vacancy_service_stub_class(self._channel)
        auth_service_stub = self.auth_service_stub_class(self._channel)
        # stub = self.stub_class(self._channel)
        # self.client = GrpcClient(stub)
        self.client = {
            "authClient":GrpcClient(auth_service_stub),
            "vacancyClient":GrpcClient(vacancy_service_stub),
        }

    def stop(self, force=False):
        self._channel_closed = True
        time.sleep(1)
        self._channel.close()
        super().stop(force=True)
import time
from typing import Any, Callable
import grpc
import grpc.experimental.gevent as grpc_gevent
from grpc_interceptor import ClientInterceptor
from locust import HttpUser, User
from locust.exception import LocustError

# patch grpc so that it uses gevent instead of asyncio
grpc_gevent.init_gevent()


class LocustInterceptor(ClientInterceptor):
    def __init__(self, environment, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.env = environment

    def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        call_details: grpc.ClientCallDetails,
    ):
        response = None
        exception = None
        start_perf_counter = time.perf_counter()
        response_length = 0
        try:
            response = method(request_or_iterator, call_details)
            response_length = response.result().ByteSize()
        except grpc.RpcError as e:
            exception = e

        self.env.events.request.fire(
            request_type="grpc",
            name=call_details.method,
            response_time=(time.perf_counter() - start_perf_counter) * 1000,
            response_length=response_length,
            response=response,
            context=None,
            exception=exception,
        )
        return response


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
        interceptor = LocustInterceptor(environment=environment)
        self._channel = grpc.intercept_channel(self._channel, interceptor)

        # self.stub = self.stub_class(self._channel)
        self.client = {
            "authClient":self.auth_service_stub_class(self._channel),
            "vacancyClient":self.vacancy_service_stub_class(self._channel),
        }
            
            
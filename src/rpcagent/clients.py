import grpc
from abc import ABC

import proto.auth_service_pb2_grpc as auth_service_grpc
import proto.auth_service_pb2 as auth_service
import proto.rpc_create_vacancy_pb2_grpc as rpc_create_vacancy_grpc
import proto.rpc_create_vacancy_pb2 as rpc_create_vacancy
import proto.rpc_signin_user_pb2_grpc as rpc_signin_user_grpc
# import proto.rpc_signin_user_pb2 as rpc_signin_user
import proto.rpc_signup_user_pb2_grpc as rpc_signup_user_grpc
import proto.rpc_signup_user_pb2 as rpc_signup_user
import proto.rpc_update_vacancy_pb2_grpc as rpc_update_vacancy_grpc
import proto.rpc_update_vacancy_pb2 as rpc_update_vacancy
import proto.user_pb2_grpc as user_grpc
import proto.user_pb2 as user
import proto.vacancy_pb2_grpc as vacancy_grpc
import proto.vacancy_pb2 as vacancy
import proto.vacancy_service_pb2_grpc as vacancy_service_grpc
import proto.vacancy_service_pb2 as vacancy_service

class BaseClient(ABC):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        # instantiate a channel
        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.port))

class AuthClient(BaseClient):
    def __init__(self, host, port):
        super().__init__(host, port)

        # bind the client and the server
        self.stub = auth_service_grpc.AuthServiceStub(self.channel)

    def signin(self, credentials):
        """
        Client function to call the rpc for GetServerResponse
        """
        return self.stub.SignInUser(credentials)
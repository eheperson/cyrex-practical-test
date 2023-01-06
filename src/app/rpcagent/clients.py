from abc import ABC

import proto.auth_service_pb2_grpc as auth_service_grpc
import proto.vacancy_service_pb2_grpc as vacancy_service_grpc

class BaseClient(ABC):
    def __init__(self, channel):
        self.channel = channel

class AuthServiceClient(BaseClient):
    def __init__(self, channel):
        super().__init__(channel)

        # bind the client and the server
        self.stub = auth_service_grpc.AuthServiceStub(self.channel)

    def sign_in_user(self, credentials):
        return self.stub.SignInUser(credentials)

    def sign_out_user(self):
        pass

    def verify_email(self):
        pass


class VacancyServiceClient(BaseClient):
    def __init__(self, channel):
        super().__init__(channel)

        # bind the client and the server
        self.stub = vacancy_service_grpc.VacancyServiceStub(self.channel)

    def create_vacancy(self, message):
        return self.stub.CreateVacancy(message)

    def get_vacancy(self, message):
        return self.stub.GetVacancy(message)

    def get_vacancies(self, message):
        return self.stub.GetVacancies(message)

    def update_vacancy(self, message):
        return self.stub.UpdateVacancy(message)

    def delete_vacancy(self, message):
        return self.stub.DeleteVacancy(message)

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

    def signInUser(self, credentials):
        """
        Client function to call the rpc
        """
        return self.stub.SignInUser(credentials)

    def signOutUser(self):
        pass

    def verifyEmail(self):
        pass


class VacancyServiceClient(BaseClient):
    def __init__(self, channel):
        super().__init__(channel)

        # bind the client and the server
        self.stub = vacancy_service_grpc.VacancyServiceStub(self.channel)

    def createVacancy(self, message):
        """
        Client function to call the rpc
        """
        return self.stub.CreateVacancy(message)

    def getVacancy(self, message):
        """
        Client function to call the rpc
        """
        return self.stub.GetVacancy(message)

    def getVacancies(self, message):
        """
        Client function to call the rpc
        """
        return self.stub.GetVacancies(message)

    def updateVacancy(self, message):
        """
        Client function to call the rpc
        """
        return self.stub.UpdateVacancy(message)

    def deleteVacancy(self, message):
        """
        Client function to call the rpc
        """
        return self.stub.DeleteVacancy(message)

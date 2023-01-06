import gevent
from rpcagent import locust
from locust import task
from dotenv import load_dotenv
import os

from rpcagent.clients import AuthServiceClient, VacancyServiceClient
from rpcagent.messages import Messages


rootDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
dotenvPath = os.path.join(rootDir, ".env")
load_dotenv(dotenvPath)


credentials = [
    {"email": os.getenv("USER_1_EMAIL"), "password": os.getenv("USER_1_PASSWORD")},
    {"email": os.getenv("USER_2_EMAIL"), "password": os.getenv("USER_2_PASSWORD")},
    {"email": os.getenv("USER_3_EMAIL"), "password": os.getenv("USER_3_PASSWORD")}
]
import rpcagent.proto.auth_service_pb2_grpc as auth_service_grpc
import rpcagent.proto.rpc_signin_user_pb2 as rpc_signin_user

""" TODO
1. Every locust user should login with one of the user credentials created in pre-
requirements. 
2. In a recurring flow every locust user should execute the following actions every 30 
seconds: 
    a. Create a vacancy with pseudo-random data 
    b. Update one or more fields in that vacancy 
    c. Fetch that specific vacancy 
    d. Delete the vacancy 
    
3. In the background the locust user should fetch a list of all vacancies available on the server 
every 45 seconds.


Report the response times of the gRPC request in locust as well as any errors that would be 
returned by the gRPC server. 
Please submit your resulting code in a zip or share a GitHub link. 
 
"""


class HelloGrpcUser(locust.GrpcUser):
    task_set=None
    host = "vacancies.cyrextech.net:7823"
    # authClient = AuthServiceClient(host='vacancies.cyrextech.net', port=7823)
    stub_class =auth_service_grpc.AuthServiceStub
    
    @task
    def loginUsers(self):
        for c in credentials:
            # message = Messages.signInUser(email=c["email"], password=c["password"])
            message = rpc_signin_user.SignInUserInput(email=c["email"], password=c["password"])
            result = self.stub.SignInUser(message)
            print(f'{result}')

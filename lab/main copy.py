import gevent
from rpcagent import locust
from locust import task, TaskSet, SequentialTaskSet, constant, constant_pacing
import logging
from dotenv import load_dotenv
import os

from rpcagent.clients import AuthServiceClient, VacancyServiceClient
from rpcagent.messages import Messages
from rpcagent.utils import RandomText

rootDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
dotenvPath = os.path.join(rootDir, ".env")
load_dotenv(dotenvPath)


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

USER_CREDENTIALS = [
    (os.getenv("USER_1_EMAIL"), os.getenv("USER_1_PASSWORD")),
    (os.getenv("USER_2_EMAIL"), os.getenv("USER_2_PASSWORD")),
    (os.getenv("USER_3_EMAIL"), os.getenv("USER_3_PASSWORD"))
]
vacancyId = None

class FetchVacancies(TaskSet):
    # wait_time = constant_pacing(10)
    @task
    def fetch_vacancies(self):
        getVacanciesMessage = Messages.getVacancies(page=100)
        res = self.client["vacancyClient"].getVacancies(getVacanciesMessage)
        logging.info("Vacancy is created zzzzzzzzzwith { %s }", res.vacancy)
        self.interrupt(reschedule=False)


class UserActions(SequentialTaskSet):
    @task
    def create_vacancy(self):
        createVacancyMessage = Messages.createVacancy(
            country=RandomText.lowercase(8),
            description=RandomText.lowercase(8),
            division=2,
            title=RandomText.lowercase(8)
        )
        global vacancyId
        res = self.client["vacancyClient"].createVacancy(createVacancyMessage)
        vacancyId = res.vacancy.Id
        logging.info("Vacancy is created with { %s }", res.vacancy)
        # self.interrupt(reschedule=False)

    @task
    def update_vacancy(self):
        global vacancyId
        updateVacancyMessage = Messages.updateVacancy(id=vacancyId, title=RandomText.lowercase(8))
        res = self.client["vacancyClient"].updateVacancy(updateVacancyMessage)
        logging.info("Vacancy is updated with { %s }", res.vacancy)
        # self.interrupt(reschedule=False)

    @task
    def fetch_vacancy(self):
        global vacancyId
        getVacancyMessage = Messages.getVacancy(id=vacancyId)
        res = self.client["vacancyClient"].getVacancy(getVacancyMessage)
        logging.info("Vacancy is fetched { %s }", res.vacancy)
        # self.interrupt(reschedule=False)

    @task
    def delete_vacancy(self):
        global vacancyId
        deleteVacancyMessage = Messages.deleteVacancy(id=vacancyId)
        res = self.client["vacancyClient"].deleteVacancy(deleteVacancyMessage)
        logging.info("Vacancy is deleted { %s }", res.success)
        self.interrupt(reschedule=False)


class LoginWithUniqueUsersTest(locust.GrpcUser):
    tasks=[UserActions, FetchVacancies]
    host = "vacancies.cyrextech.net:7823"
    vacancy_service_stub_class=VacancyServiceClient
    auth_service_stub_class=AuthServiceClient

    email = "NOT_FOUND"
    password = "NOT_FOUND"

    def on_start(self):
        if len(USER_CREDENTIALS) > 0:
            self.email, self.password = USER_CREDENTIALS.pop()

    @task
    def login(self):
        credentials = Messages.signInUser(email=self.email, password=self.password)
        self.client["authClient"].signInUser(credentials=credentials)
        logging.info('Login with %s email and %s password', self.email, self.password)

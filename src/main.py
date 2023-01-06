from locust import task, SequentialTaskSet, constant
import logging
from rpcagent.clients import AuthServiceClient, VacancyServiceClient
from rpcagent.messages import Messages
from rpcagent.utils import RandomText, getUser
from rpcagent.locust import GrpcUser

vacancyId = None
class LoginWithUsers(SequentialTaskSet):
    wait_time = constant(30)
    email = "NOT_FOUND"
    password = "NOT_FOUND"
    def on_start(self):
            # if len(USER_CREDENTIALS) > 0:
            self.email, self.password = getUser()
            
            credentials = Messages.signInUser(email=self.email, password=self.password)
            self.client["authClient"].signInUser(credentials=credentials)
            logging.info('Login with %s email and %s password', self.email, self.password)
    
    # @task
    # def login(self):
    #     credentials = Messages.signInUser(email=self.email, password=self.password)
    #     self.client["authClient"].signInUser(credentials=credentials)
    #     logging.info('Login with %s email and %s password', self.email, self.password)
    #     time.sleep(10)

    @task
    class VacancyLoad(SequentialTaskSet):
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

class FetchVacancies(GrpcUser):
    host = "vacancies.cyrextech.net:7823"
    vacancy_service_stub_class=VacancyServiceClient 
    auth_service_stub_class=AuthServiceClient
    wait_time = constant(45)
    weight=1
    @task
    def eeee(self):
        print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    # @task
    # def fetch_vacancies(self):
    #     getVacanciesMessage = Messages.getVacancies(page=100)
    #     res = self.client["vacancyClient"].getVacancies(getVacanciesMessage)
    #     logging.info("Vacancy is created zzzzzzzzzwith { %s }", res.vacancy)
    #     self.interrupt(reschedule=False)


class LoginWithUniqueUsersTest(GrpcUser):
    host = "vacancies.cyrextech.net:7823"
    tasks=[LoginWithUsers]
    weight=3
    vacancy_service_stub_class=VacancyServiceClient 
    auth_service_stub_class=AuthServiceClient

import logging
import time

from locust import task, SequentialTaskSet, constant
from rpcagent.clients import AuthServiceClient, VacancyServiceClient
from rpcagent.locust import GrpcUser
from rpcagent.messages import Messages
from rpcagent.utils import RandomText, get_user

vacancy_id = None

class LoginWithUsers(SequentialTaskSet):
    wait_time = constant(30)
    email = "NOT_FOUND"
    password = "NOT_FOUND"
    def on_start(self):
        self.email, self.password = get_user()
        
        credentials = Messages.sign_in_user(email=self.email, password=self.password)
        self.client["authClient"].sign_in_user(credentials=credentials)
        logging.info('Login with %s email and %s password', self.email, self.password)

    @task
    class VacancyLoad(SequentialTaskSet):
        @task
        def create_vacancy(self):
            global vacancy_id
            create_vacancy_message = Messages.create_vacancy(
                country=RandomText.lowercase(8),
                description=RandomText.lowercase(8),
                division=2,
                title=RandomText.lowercase(8)
            )
            res = self.client["vacancyClient"].create_vacancy(create_vacancy_message)
            vacancy_id = res.vacancy.Id
            logging.info("Vacancy is created with { %s }", res.vacancy)

        @task
        def update_vacancy(self):
            global vacancy_id
            update_vacancy_message = Messages.update_vacancy(id=vacancy_id, title=RandomText.lowercase(8))
            res = self.client["vacancyClient"].update_vacancy(update_vacancy_message)
            logging.info("Vacancy is updated with { %s }", res.vacancy)

        @task
        def fetch_vacancy(self):
            global vacancy_id
            get_vacancy_message = Messages.get_vacancy(id=vacancy_id)
            res = self.client["vacancyClient"].get_vacancy(get_vacancy_message)
            logging.info("Vacancy is fetched { %s }", res.vacancy)

        @task
        def delete_vacancy(self):
            global vacancy_id
            delete_vacancy_message = Messages.delete_vacancy(id=vacancy_id)
            res = self.client["vacancyClient"].delete_vacancy(delete_vacancy_message)
            logging.info("Vacancy is deleted { %s }", res.success)
            self.interrupt(reschedule=False)


class FetchVacancies(GrpcUser):
    host = "vacancies.cyrextech.net:7823"
    vacancy_service_stub_class=VacancyServiceClient 
    auth_service_stub_class=AuthServiceClient
    wait_time = constant(44)
    weight=1
    @task
    def fetch_vacancies(self):
        if not self._channel_closed:
            get_vacancies_message = Messages.get_vacancies(limit=100)
            res = self.client["vacancyClient"].get_vacancies(get_vacancies_message)
            logging.info("vacancies are fetched : {%s} ", str(res))
        time.sleep(1)


class LoginWithUniqueUsersTest(GrpcUser):
    host = "vacancies.cyrextech.net:7823"
    tasks=[LoginWithUsers]
    weight=3
    vacancy_service_stub_class=VacancyServiceClient 
    auth_service_stub_class=AuthServiceClient

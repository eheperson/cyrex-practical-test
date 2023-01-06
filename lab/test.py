from dotenv import load_dotenv
import os

from rpcagent.clients import AuthServiceClient, VacancyServiceClient
from rpcagent.messages import Messages

rootDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
dotenvPath = os.path.join(rootDir, ".env")
load_dotenv(dotenvPath)

user1 = {
    "email": os.getenv("USER_1_EMAIL"),
    "password": os.getenv("USER_1_PASSWORD")
}
user2 = {
    "email": os.getenv("USER_2_EMAIL"),
    "password": os.getenv("USER_2_PASSWORD")
}
user3 = {
    "email": os.getenv("USER_3_EMAIL"),
    "password": os.getenv("USER_3_PASSWORD")
}

credentials = [
    {"email": os.getenv("USER_1_EMAIL"), "password": os.getenv("USER_1_PASSWORD")},
    {"email": os.getenv("USER_2_EMAIL"), "password": os.getenv("USER_2_PASSWORD")},
    {"email": os.getenv("USER_3_EMAIL"), "password": os.getenv("USER_3_PASSWORD")}
]


from rpcagent.messages import Messages
from rpcagent.clients import VacancyServiceClient

if __name__ == '__main__':
    # authClient = AuthServiceClient(host='vacancies.cyrextech.net', port=7823)
    # for c in credentials:
    #     message = Messages.signInUser(email=c["email"], password=c["password"])
    #     result = authClient.signInUser(credentials=message)
    #     print(f'{result}')

    vacancyClient = VacancyServiceClient(host='vacancies.cyrextech.net', port=7823)

    createVacancy = Messages.createVacancy(
        country="eeee",
        description="ererer",
        division=2,
        title="erfftgffddddfffee"
    )
    print(createVacancy)
    created = vacancyClient.createVacancy(createVacancy)
    print(created)

    delVac = Messages.deleteVacancy(id="63b5cf4dd99d387c3d3b290b")
    print(delVac)
    print(vacancyClient.deleteVacancy(delVac))

    getVacs = Messages.getVacancies(page=2)
    print(getVacs)
    print(vacancyClient.getVacancies(getVacs))

    # getVac = Messages.getVacancy(id="asdasdasd")
    # print(getVac)

    # updateVac = Messages.updateVacancy(id="adasd", title="dddddd")
    # print(updateVac)
from dotenv import load_dotenv
import os

from rpcagent.clients import AuthClient
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


if __name__ == '__main__':
    authClient = AuthClient(host='vacancies.cyrextech.net', port=7823)
    for c in credentials:
        message = Messages.signinUser(email=c["email"], password=c["password"])
        result = authClient.signin(credentials=message)
        print(f'{result}')
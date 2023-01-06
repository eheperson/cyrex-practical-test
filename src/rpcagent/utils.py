import random
import string
from dotenv import load_dotenv
import os

class RandomText:
    @classmethod
    def lowercase(cls, length:int, repeated:bool=False):
        if repeated:
            result = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
        else:
            result = ''.join(random.sample(string.ascii_lowercase, length))
        return result

    @classmethod
    def uppercase(cls, length:int, repeated:bool=False):
        if repeated:
            result = ''.join(random.choice(string.ascii_uppercase) for i in range(length))
        else:
            result = ''.join(random.sample(string.ascii_uppercase, length))
        return result

    @classmethod
    def randomcase(cls, length:int, repeated:bool=False):
        if repeated:
            result = ''.join(random.choice(string.ascii_letters) for i in range(length))
        else:
            result = ''.join(random.sample(string.ascii_letters, length))
        return result

    @classmethod
    def fromstr(cls, length:int, baseStr:str):
        result = ''.join((random.choice(baseStr) for i in range(length)))
        return result

counter = 1
def getUser():
    rootDir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dotenvPath = os.path.join(rootDir, ".env")
    load_dotenv(dotenvPath)
    global counter
    USER_CREDENTIALS = [
        (os.getenv("USER_1_EMAIL"), os.getenv("USER_1_PASSWORD")),
        (os.getenv("USER_2_EMAIL"), os.getenv("USER_2_PASSWORD")),
        (os.getenv("USER_3_EMAIL"), os.getenv("USER_3_PASSWORD"))
    ]
    user = USER_CREDENTIALS[counter%3-1]
    counter += 1
    return user
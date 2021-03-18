import requests
from enum import Enum


class ssu_login_status(Enum):
    success = 1
    failure = 0


class ssu_session:
    def __init__(self):
        self.__session = requests.session()

    def login(self, username, password):
        login_url = "https://myclass.ssu.ac.kr/login/index.php"
        response = self.__session.post(login_url, data={'username': username, 'password': password})

        return ssu_login_status.success

    def get(self, url):
        self.__session.get(url)

    def post(self, url, data):
        self.__session.post(url, data)

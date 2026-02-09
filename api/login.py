import requests
from config.config import BASE_URL, LOGIN_DATA

class LoginAPI:
    def __init__(self):
        self.url_verify = BASE_URL + "/api/captchaImage"
        self.url_login = BASE_URL + "/api/login"

    def get_verify_code(self, session):
        if session is None:
            raise ValueError("session 不能为空！")
        response = session.get(url=self.url_verify, verify=False)
        uuid = response.json().get("uuid")
        print(f"LoginAPI.get_verify_code session ID: {id(session)}")
        return uuid

    def login(self, test_data, session):
        if session is None:
            raise ValueError("session 不能为空！")
        if test_data is None:
            test_data = LOGIN_DATA.copy()

        uuid = self.get_verify_code(session)
        test_data["uuid"] = uuid

        res_login = session.post(url=self.url_login, json=test_data, verify=False)
        print(f"LoginAPI.login session ID: {id(session)}")
        return res_login

    def get_token(self, test_data, session):
        if session is None:
            raise ValueError("session 不能为空！")
        if test_data is None:
            test_data = LOGIN_DATA.copy()

        resp = self.login(test_data, session)
        print(f"LoginAPI.get_token session ID: {id(session)}")
        print("登录响应:", resp.json())
        resp_json = resp.json()
        token = resp_json.get("token")
        return token
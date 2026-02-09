import requests
import config

#封装接口
class LoginAPI:
    #初始化
    def __init__(self):
        self.url_verify=config.BASE_URL + "/api/captchaImage"
        self.url_login=config.BASE_URL + "/api/login"
    #验证码
    def get_verify_code(self):
        return requests.get(url=self.url_verify,verify=False)
    #登录
    def login(self,test_data):
        return requests.post(url=self.url_login,json=test_data,verify=False)

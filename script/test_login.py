import requests
from api.login import LoginAPI
import pytest
import json
from config.config import BASE_PATH

#读取json文件
def build_data(json_file):
    #定义空列表
    test_data = []
    with open(json_file,"r",encoding="utf-8") as f:
        #加载json文件数据
        json_data = json.load(f)
        #循环遍历数据
        for case_data in json_data:
            #将[{},{}]转换为[(),()]
            username=case_data.get("username")
            password = case_data.get("password")
            status = case_data.get("status")
            message = case_data.get("message")
            code = case_data.get("code")
            #追加到空列表
            test_data.append((username,password,status,message,code))
    return test_data
class TestLoginAPI:
    #前置条件
    def setup_method(self):
        #实例化接口
        self.api_login=LoginAPI()
        self.session = requests.Session()

    #后置条件
    def teardown(self):
        self.session.close()

    #登录
    @pytest.mark.parametrize("username,password,status,message,code",
                             build_data(json_file=BASE_PATH + "/data/login.json"))
    def test01_login_success(self,username,password,status,message,code):
        uuid = self.api_login.get_verify_code(session=self.session)
        login_data = {
            "username":username,
            "password": password,
            "code": "2",
            "uuid": uuid
        }
        res_login = self.api_login.login(test_data=login_data, session=self.session)
        print(res_login.status_code)

        #断言
        #状态码200
        assert status == res_login.status_code
        #包含成功
        assert message in res_login.text
        #json中code值为200
        assert code == res_login.json().get("code")

import requests
from api.login import LoginAPI
import pytest
import json
import config

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
    uuid=None
    #前置条件
    def setup_method(self):
        #实例化接口
        self.api_login=LoginAPI()
        #获取验证码
        res_code = self.api_login.get_verify_code()
        TestLoginAPI.uuid=res_code.json().get("uuid")
    #后置条件
    def teardown(self):
        pass
    #登陆
    @pytest.mark.parametrize("username,password,status,message,code",
                             build_data(json_file=config.BASE_PATH + "/data/login.json"))
    def test01_login_success(self,username,password,status,message,code):
        login_data = {
            "username":username,
            "password": password,
            "code": "2",
            "uuid": TestLoginAPI.uuid
        }
        res_login = self.api_login.login(test_data=login_data)
        print(res_login.status_code)

        #断言
        #状态码200
        assert status == res_login.status_code
        #包含成功
        assert message in res_login.text
        #json中code值为200
        assert code == res_login.json().get("code")

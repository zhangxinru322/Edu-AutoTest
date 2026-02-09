import requests
from api.login import LoginAPI
from api.contract import ContractAPI
import pytest
import json
import config

#打开合同文件
file = open(config.BASE_PATH + "/data/test.pdf","rb")

class TestUpLoadContractAPI:
    uuid = None
    TOKEN = None
    #前置条件
    def setup_method(self):
        #实例化接口
        self.api_login = LoginAPI()
        self.api_contract = ContractAPI()
        # 获取验证码
        res_code = self.api_login.get_verify_code()
        print(res_code.status_code)
        TestUpLoadContractAPI.uuid = res_code.json().get("uuid")
        # 登录成功
        login_data = {
            "username":"admin",
            "password":"HM_2023_test",
            "code":2,
            "uuid":res_code.json().get("uuid")
        }
        res_login = self.api_login.login(test_data=login_data)
        print(res_login.status_code)
        TestUpLoadContractAPI.TOKEN = res_login.json().get("token")
    #后置条件
    def teardown(self):
        pass

    #上传合同文件成功
    def test01_add_contract_success(self):
        res_upload = self.api_contract.upload_contract(test_data=file,token=TestUpLoadContractAPI.TOKEN)
        #断言
        #状态码200
        assert 200 == res_upload.status_code
        #包含成功
        assert "成功" in res_upload.text
        #json值为200
        assert 200 == res_upload.json().get("code")
    #上传合同文件失败（未登录）
    def test02_add_contract_fail(self):
        res_upload = self.api_contract.upload_contract(test_data=file,token="xxx")
        # 断言
        # 状态码200
        assert 200 == res_upload.status_code
        # 包含失败
        assert "失败" in res_upload.text
        # json值为401
        assert 401 == res_upload.json().get("code")
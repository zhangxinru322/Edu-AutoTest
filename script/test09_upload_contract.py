import requests
from api.contract import ContractAPI
import pytest
import json
from config.config import BASE_PATH
#打开合同文件
file = open(BASE_PATH + "/data/test.pdf","rb")

class TestUpLoadContractAPI:
    #前置条件
    def setup_method(self):
        pass
    #后置条件
    def teardown(self):
        pass

    #上传合同文件成功
    def test01_add_contract_success(self):
        self.contract_api = ContractAPI(with_token=True)
        res_upload = self.contract_api.upload_contract(test_data=file)
        print(res_upload.json())
        #断言
        #状态码200
        assert 200 == res_upload.status_code
        #包含成功
        assert "成功" in res_upload.text
        #json值为200
        assert 200 == res_upload.json().get("code")
    #上传合同文件失败（未登录）
    def test02_add_contract_fail(self):
        self.contract_api = ContractAPI(with_token=False)
        res_upload = self.contract_api.upload_contract(test_data=file)
        print(res_upload.json())
        # 断言
        # 状态码200
        assert 200 == res_upload.status_code
        # 包含失败
        assert "失败" in res_upload.text
        # json值为401
        assert 401 == res_upload.json().get("code")
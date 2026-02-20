import requests
from api.contract import ContractAPI
import pytest
from config.config import BASE_PATH

#打开合同文件
def get_contract_file():
    return open(BASE_PATH + "/data/test.pdf", "rb")

class TestUpLoadContractAPI:
    #前置条件
    def setup_method(self):
        self.session = requests.Session()

    # 后置条件
    def teardown(self):
        self.session.close()

    #上传合同文件成功
    def test01_add_contract_success(self):
        self.contract_api = ContractAPI(with_token=True)
        # 重新打开文件，确保内容完整
        file = get_contract_file()
        res_upload = self.contract_api.upload_contract(test_data = file)
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
        file = get_contract_file()
        res_upload = self.contract_api.upload_contract(test_data = file)
        print(res_upload.json())
        # 断言
        # 状态码200
        assert 200 == res_upload.status_code
        # 包含失败
        assert "失败" in res_upload.text
        # json值为401
        assert 401 == res_upload.json().get("code")
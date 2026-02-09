import requests
import config

class ContractAPI:
    #初始化
    def __init__(self):
        self.url_upload=config.BASE_URL + "/api/common/upload"
        self.url_contract=config.BASE_URL + "/api/contract"
    #新增合同
    def upload_contract(self,test_data,token):
        return requests.post(url=self.url_upload,files={"file":test_data},headers={"Authorization":token},verify=False)
    def add_contract(self,test_data,token):
        return requests.post(url=self.url_contract,headers={"Authorization":token},json=test_data,verify=False)
import requests
from api.login import LoginAPI
from config.config import BASE_URL, HEADERS

class ContractAPI:
    #初始化
    def __init__(self, with_token=True):
        # 只在这里创建一次session，全程复用
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        print(f"ContractAPI.__init__ session ID: {id(self.session)}")

        self.url_upload=BASE_URL + "/api/common/upload"
        self.url_contract=BASE_URL + "/api/contract"
        if with_token:
            login_api = LoginAPI()
            token = login_api.get_token(test_data=None, session=self.session)
            print(f"ContractAPI 拿到token后的session ID: {id(self.session)}")

            if token:
                self.session.headers["Authorization"] = f"Bearer {token}"
    #新增合同
    def upload_contract(self,test_data):
        return self.session.post(url=self.url_upload,files={"file":test_data},verify=False)
    def add_contract(self,test_data):
        return self.session.post(url=self.url_contract,json=test_data,verify=False)
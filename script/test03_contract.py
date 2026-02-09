import requests
from api.login import LoginAPI
from api.course import CourseAPI
from api.contract import ContractAPI

class TestContract:
    #初始化
    token=None
    fileName=None
    #前置条件
    def setup_method(self):
        #实例化接口
        self.api_login=LoginAPI()
        self.api_course=CourseAPI()
        self.api_contract=ContractAPI()

    #后置条件
    def teardown(self):
        pass
    #1.登陆成功
    def test01_login_success(self):
        #获取验证码
        res_code=self.api_login.get_verify_code()
        print(res_code.status_code)
        print(res_code.text)
        #打印uuid
        print(res_code.json().get("uuid"))
        #登录
        login_data = {
            "username": "admin",
            "password": "HM_2023_test",
            "code": "2",
            "uuid": res_code.json().get("uuid")
        }
        res_login=self.api_login.login(test_data=login_data)
        print(res_login.status_code)
        print(res_login.json())
        TestContract.token=res_login.json().get("token")
        print(res_login.json().get("token"))
    #2.课程新增成功
    def test02_add_course_success(self):
        #新增课程
        add_data = {
            "name": "课设",
            "subject": "6",
            "price": 2333,
            "applicablePerson": "1",
            "info": "null"
        }
        res_course=self.api_course.add_course(test_data=add_data,token=TestContract.token)
        print(res_course.status_code)
        print(res_course.json())
    #3.合同文件上传成功
    def test03_upload_contract_success(self):
        #新增文件
        f = open("../data/test.pdf","rb")
        res_upload=self.api_contract.upload_contract(test_data=f,token=TestContract.token)
        TestContract.fileName=print(res_upload.json().get("fileName"))
        print(res_upload.json().get("fileName"))
    #4.合同新增成功
    def test04_add_contract_success(self):
        contract_data={
            "name":"张三",
            "phone":"13612345678",
            "contractNo":"348",
            "subject":"3",
            "courseId":1505,
            "channel":"1",
            "activityId":"",
            "fileName":TestContract.fileName
        }
        res_contract=self.api_contract.add_contract(test_data=contract_data,token=TestContract.token)
        print(res_contract.json())
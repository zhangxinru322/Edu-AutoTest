import requests
from api.contract import ContractAPI
import pytest
import json
from config.config import BASE_PATH

def build_data(json_file, case_type=None):
    #创建空列表
    test_data=[]
    #打开json文件
    with open(json_file,"r",encoding="utf-8") as f:
        #加载数据
        json_data = json.load(f)
        #循环遍历数据
        for case_data in json_data:
            # 如果指定了case_type，只处理对应类型的用例
            if case_type and case_data.get("case_type") != case_type:
                continue
            #将[{},{}]转换为[(),()]
            name = case_data.get("name")
            phone = case_data.get("phone")
            contractNo = case_data.get("contractNo")
            subject = case_data.get("subject")
            courseId = case_data.get("courseId")
            channel = case_data.get("channel")
            activityId = case_data.get("activityId")
            status = case_data.get("status")
            message = case_data.get("message")
            code = case_data.get("code")
            #追加到空列表
            test_data.append((name,phone,contractNo,subject,courseId,channel,activityId,status,message,code))
    return test_data

class TestAddContractAPI:
    #前置条件
    def setup_method(self):
        self.session = requests.Session()
    #后置条件
    def teardown(self):
        self.session.close()
    #添加合同成功
    @pytest.mark.parametrize("name,phone,contractNo,subject,courseId,channel,activityId,status,message,code",
                             build_data(json_file=BASE_PATH + "/data/contract.json", case_type="success"))
    def test01_add_course_success(self,name,phone,contractNo,subject,courseId,channel,activityId,status,message,code):
        self.api_contract = ContractAPI(with_token=True)
        contract_data = {
            "name": name,
            "phone": phone,
            "contractNo": contractNo,
            "subject": subject,
            "courseId": courseId,
            "channel": channel,
            "activityId": activityId
        }
        res_contract = self.api_contract.add_contract(test_data=contract_data)
        print(res_contract.json())
        #断言
        #状态码200
        assert status == res_contract.status_code
        #包含成功
        assert message in res_contract.text
        #json中code值为200
        assert code == res_contract.json().get("code")
    #添加合同失败（未登录）
    @pytest.mark.parametrize("name,phone,contractNo,subject,courseId,channel,activityId,status,message,code",
                             build_data(json_file=BASE_PATH + "/data/contract.json", case_type="fail"))
    def test02_add_course_fail(self,name,phone,contractNo,subject,courseId,channel,activityId,status,message,code):
        self.api_contract = ContractAPI(with_token=False)
        contract_data={
            "name":name,
            "phone":phone,
            "contractNo":contractNo,
            "subject":subject,
            "courseId":courseId,
            "channel":channel,
            "activityId":activityId
        }
        res_contract=self.api_contract.add_contract(test_data=contract_data)
        print(res_contract.json())
        # 断言
        # 状态码200
        assert status == res_contract.status_code
        # 包含失败
        assert message in res_contract.text
        # json中code值为401
        assert code == res_contract.json().get("code")
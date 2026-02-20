import requests
from api.contract import ContractAPI
import pytest
from config.config import TEST_CASES  # 导入YAML中的测试用例配置

# 重构数据构建函数：从YAML读取用例，不再依赖JSON文件
def build_data(case_module, case_type=None):
    """
    从YAML配置的TEST_CASES中读取指定模块、指定类型的用例数据
    :param case_module: 用例模块名（如"contract"）
    :param case_type: 用例类型（如"success"/"fail"）
    :return: 格式化的测试数据列表
    """
    test_data = []
    # 从YAML的TEST_CASES中获取合同相关用例
    contract_cases = TEST_CASES.get(case_module, {})

    # 循环遍历所有合同用例，筛选指定类型
    for case_key, case_data in contract_cases.items():
        # 如果指定了case_type，只处理对应类型的用例
        if case_type and case_data.get("case_type") != case_type:
            continue
        # 提取用例参数
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

        # 追加到测试数据列表
        test_data.append((name, phone, contractNo, subject, courseId, channel, activityId, status, message, code))
    return test_data

class TestAddContractAPI:
    # 前置条件：初始化session
    def setup_method(self):
        self.session = requests.Session()

    # 后置条件：关闭session（改为teardown_method，和setup_method配对）
    def teardown_method(self):
        self.session.close()

    # 添加合同成功
    @pytest.mark.parametrize("name,phone,contractNo,subject,courseId,channel,activityId,status,message,code",
                             build_data(case_module="contract", case_type="success"))
    def test01_add_contract_success(self, name, phone, contractNo, subject, courseId, channel, activityId, status,
                                    message, code):
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

        # 断言
        assert status == res_contract.status_code  # 断言响应状态码
        assert message in res_contract.text  # 断言响应包含指定消息
        assert code == res_contract.json().get("code")  # 断言业务码

    # 添加合同失败（合同号已存在）
    @pytest.mark.parametrize("name,phone,contractNo,subject,courseId,channel,activityId,status,message,code",
                             build_data(case_module="contract", case_type="failed"))
    def test02_add_contract_fail(self, name, phone, contractNo, subject, courseId, channel, activityId, status,
                                    message, code):
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

        # 断言
        assert status == res_contract.status_code  # 断言响应状态码
        assert message in res_contract.text  # 断言响应包含指定消息
        assert code == res_contract.json().get("code")  # 断言业务码

    # 添加合同失败（未登录）
    @pytest.mark.parametrize("name,phone,contractNo,subject,courseId,channel,activityId,status,message,code",
                             build_data(case_module="contract", case_type="fail"))
    def test03_add_contract_fail(self, name, phone, contractNo, subject, courseId, channel, activityId, status, message,
                                 code):
        self.api_contract = ContractAPI(with_token=False)
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

        # 断言
        assert status == res_contract.status_code
        assert message in res_contract.text
        assert code == res_contract.json().get("code")
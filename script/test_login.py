import requests
from api.login import LoginAPI
import pytest
from config.config import TEST_CASES

def build_data(case_module, case_type=None):
    """
    从YAML的TEST_CASES中读取指定模块、指定类型的用例数据
    :param case_module: 用例模块名（如"login"）
    :param case_type: 用例类型（如"success"/"fail"）
    :return: 格式化的测试数据列表
    """
    test_data = []
    # 从YAML获取指定模块的所有用例
    module_cases = TEST_CASES.get(case_module, {})

    # 遍历：items()返回(key, value)，需要解构出真正的用例数据value
    for case_key, case_data in module_cases.items():
        # 筛选指定类型的用例
        if case_type and case_data.get("case_type") != case_type:
            continue

        # 3. 提取登录用例参数
        username = case_data.get("username")
        password = case_data.get("password")
        status = case_data.get("status")
        message = case_data.get("message")
        code = case_data.get("code")

        # 4. 追加到测试数据列表（过滤空值，避免参数异常）
        if all([username, password, status, message, code]):
            test_data.append((username, password, status, message, code))

    print(f"{case_module}模块筛选出 {len(test_data)} 个有效用例")
    return test_data


class TestLoginAPI:
    # 前置条件
    def setup_method(self):
        self.session = requests.Session()
        self.api_login = LoginAPI()  # 实例化登录接口

    # 后置条件
    def teardown_method(self):
        self.session.close()

    # 登录成功用例
    @pytest.mark.parametrize("username,password,status,message,code",
                             build_data(case_module="login", case_type="success"))
    def test01_login_success(self, username, password, status, message, code):
        # 获取验证码uuid
        uuid = self.api_login.get_verify_code(session=self.session)
        # 构造登录参数
        login_data = {
            "username": username,
            "password": password,
            "code": "2",
            "uuid": uuid
        }
        # 发送登录请求
        res_login = self.api_login.login(test_data=login_data, session=self.session)
        print(f"登录响应状态码：{res_login.status_code}，响应内容：{res_login.text}")

        # 断言
        assert res_login.status_code == status
        assert message in res_login.text
        assert res_login.json().get("code") == code

    # 登录失败用例
    @pytest.mark.parametrize("username,password,status,message,code",
                             build_data(case_module="login", case_type="fail"))
    def test02_login_fail(self, username, password, status, message, code):
        # 获取验证码uuid
        uuid = self.api_login.get_verify_code(session=self.session)
        # 构造登录参数
        login_data = {
            "username": username,
            "password": password,
            "code": "2",
            "uuid": uuid
        }
        # 发送登录请求
        res_login = self.api_login.login(test_data=login_data, session=self.session)
        print(f"登录响应状态码：{res_login.status_code}，响应内容：{res_login.text}")

        # 断言
        assert res_login.status_code == status
        assert message in res_login.text
        assert res_login.json().get("code") == code
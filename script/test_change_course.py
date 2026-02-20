import requests
from api.login import LoginAPI
from api.course import CourseAPI
import pytest
from config.config import TEST_CASES

# 重构数据构建函数：从YAML读取用例，废弃JSON文件读取
def build_data(case_module, case_type):
    """
    从YAML的TEST_CASES中读取指定模块、指定类型的修改课程用例
    :param case_module: 模块名（如"course"）
    :param case_type: 用例类型（success/fail）
    :return: 格式化的测试数据列表
    """
    test_data = []
    # 获取课程模块的所有用例
    module_cases = TEST_CASES.get(case_module, {})

    # 遍历用例：解构(key, value)，确保只处理字典类型的用例数据
    for case_key, case_data in module_cases.items():
        # 筛选指定类型的用例
        if case_type and case_data.get("case_type") != case_type:
            continue

        # 提取修改课程的参数（和原JSON字段完全一致）
        id = case_data.get("id")
        name = case_data.get("name")
        subject = case_data.get("subject")
        price = case_data.get("price")
        applicablePerson = case_data.get("applicablePerson")
        status = case_data.get("status")
        message = case_data.get("message")
        code = case_data.get("code")

        # 过滤空参数，避免测试异常
        if all([id, name, subject, price, applicablePerson, status, message, code]):
            test_data.append((id, name, subject, price, applicablePerson, status, message, code))

    print(f"{case_module}模块-{case_type}类型：筛选出 {len(test_data)} 个修改课程用例")
    return test_data

class TestUpdateCourseAPI:
    TOKEN = None
    uuid = None
    session = None  # 初始化session变量

    # 前置条件：初始化session，避免teardown报错
    def setup_method(self):
        self.session = requests.Session()

    # 后置条件：规范命名为teardown_method，配对setup_method
    def teardown_method(self):
        if self.session:  # 避免session未初始化导致的报错
            self.session.close()

    # 修改课程成功
    @pytest.mark.parametrize("id,name,subject,price,applicablePerson,status,message,code",
                             build_data(case_module="change_course", case_type="success"))
    def test01_update_course_success(self, id, name, subject, price, applicablePerson, status, message, code):
        self.course_api = CourseAPI(with_token=True)
        update_data = {
            "id": id,
            "name": name,
            "subject": subject,
            "price": price,
            "applicablePerson": applicablePerson
        }
        res_update = self.course_api.update_course(test_data=update_data)
        print(f"修改课程成功响应：{res_update.json()}")

        # 断言
        assert status == res_update.status_code
        assert message in res_update.text
        assert code == res_update.json().get("code")


    # 修改课程失败（课程id不存在）
    @pytest.mark.parametrize("id,name,subject,price,applicablePerson,status,message,code",
                             build_data(case_module="change_course", case_type="failed"))
    def test02_update_course_fail(self, id, name, subject, price, applicablePerson, status, message, code):
        self.course_api = CourseAPI(with_token=True)
        update_data = {
            "id": id,
            "name": name,
            "subject": subject,
            "price": price,
            "applicablePerson": applicablePerson
        }
        res_update = self.course_api.update_course(test_data=update_data)
        print(f"修改课程失败响应：{res_update.json()}")

        # 断言
        assert status == res_update.status_code
        assert message in res_update.text
        assert code == res_update.json().get("code")

    # 修改课程失败（未登录）
    @pytest.mark.parametrize("id,name,subject,price,applicablePerson,status,message,code",
                             build_data(case_module="change_course", case_type="fail"))
    def test03_update_course_fail(self, id, name, subject, price, applicablePerson, status, message, code):
        self.course_api = CourseAPI(with_token=False)
        update_data = {
            "id": id,
            "name": name,
            "subject": subject,
            "price": price,
            "applicablePerson": applicablePerson
        }
        res_update = self.course_api.update_course(test_data=update_data)
        print(f"修改课程失败响应：{res_update.json()}")

        # 断言
        assert status == res_update.status_code
        assert message in res_update.text
        assert code == res_update.json().get("code")
import requests
from api.course import CourseAPI
import pytest
from config.config import TEST_CASES  # 导入YAML中的测试用例配置

# 重构数据构建函数：从YAML读取用例，不再依赖JSON文件
def build_data(case_module, case_type=None):
    """
    从YAML配置的TEST_CASES中读取指定模块、指定类型的用例数据
    :param case_module: 用例模块名（如"course"）
    :param case_type: 用例类型（如"success"/"fail"）
    :return: 格式化的测试数据列表
    """
    test_data = []
    # 从YAML的TEST_CASES中获取课程相关用例
    module_cases = TEST_CASES.get(case_module, {})

    # 循环遍历所有课程用例，筛选指定类型
    for case_key, case_data in module_cases.items():
        # 如果指定了case_type，只处理对应类型的用例
        if case_type and case_data.get("case_type") != case_type:
            continue

        # 提取用例参数
        name = case_data.get("name")
        subject = case_data.get("subject")
        price = case_data.get("price")
        applicablePerson = case_data.get("applicablePerson")
        status = case_data.get("status")
        message = case_data.get("message")
        code = case_data.get("code")

        # 追加到测试数据列表（过滤空值，避免参数异常）
        if all([name, subject, price, applicablePerson, status, message, code]):
            test_data.append((name, subject, price, applicablePerson, status, message, code))

    print(f" {case_module}模块-{case_type}类型：共筛选出 {len(test_data)} 个有效用例")
    return test_data

class TestAddCourseAPI:
    # 前置条件：初始化session
    def setup_method(self):
        self.session = requests.Session()

    # 后置条件：规范命名为teardown_method，和setup_method配对
    def teardown_method(self):
        self.session.close()

    # 添加课程成功
    @pytest.mark.parametrize("name,subject,price,applicablePerson,status,message,code",
                             build_data(case_module="course", case_type="success"))
    def test01_add_course_success(self, name, subject, price, applicablePerson, status, message, code):
        self.course_api = CourseAPI(with_token=True)
        add_data = {
            "name": name,
            "subject": subject,
            "price": price,
            "applicablePerson": applicablePerson
        }
        res_course = self.course_api.add_course(test_data=add_data)
        print(f"添加课程成功响应：{res_course.json()}")

        # 断言
        assert status == res_course.status_code
        assert message in res_course.text
        assert code == res_course.json().get("code")

    # 添加课程失败（未登录）
    @pytest.mark.parametrize("name,subject,price,applicablePerson,status,message,code",
                             build_data(case_module="course", case_type="fail"))
    def test02_add_course_fail(self, name, subject, price, applicablePerson, status, message, code):
        self.course_api = CourseAPI(with_token=False)
        add_data = {
            "name": name,
            "subject": subject,
            "price": price,
            "applicablePerson": applicablePerson
        }
        res_course = self.course_api.add_course(test_data=add_data)
        print(f"添加课程失败响应：{res_course.json()}")

        # 断言
        assert status == res_course.status_code
        assert message in res_course.text
        assert code == res_course.json().get("code")
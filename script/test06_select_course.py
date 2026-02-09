import requests
from api.login import LoginAPI
from api.course import CourseAPI

class TestSelectCourseAPI:
    TOKEN = None
    #前置条件
    def setup_method(self):
        self.api_login = LoginAPI()
        self.api_course = CourseAPI()
        #登录成功
        #获取验证码
        res_code = self.api_login.get_verify_code()
        #登录
        login_data = {
            "username": "admin",
            "password": "HM_2023_test",
            "code": "2",
            "uuid": res_code.json().get("uuid")
        }
        res_login = self.api_login.login(test_data=login_data)
        TestSelectCourseAPI.TOKEN = res_login.json().get("token")
    #后置条件
    def teardown(self):
        pass
    #查询课程成功
    def test01_select_course_success(self):
        response = self.api_course.select_course(test_data="?name=测试开发提升课01",token=TestSelectCourseAPI.TOKEN)
        print(response.json())
        #断言
        #状态码200
        assert 200 == response.status_code
        #包含成功
        assert "成功" in response.text
        #json中code值为200
        assert 200 == response.json().get("code")
    #查询课程失败（未登录）
    def test02_select_course_failed(self):
        response = self.api_course.select_course(test_data="?name=00",token="xxx")
        print(response.json())
        # 断言
        # 状态码200
        assert 200 == response.status_code
        # 包含失败
        assert "失败" in response.text
        # json中code值为401
        assert 401 == response.json().get("code")
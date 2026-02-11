import requests
from api.login import LoginAPI
from api.course import CourseAPI

class TestSelectCourseAPI:
    TOKEN = None
    #前置条件
    def setup_method(self):
        pass
    #后置条件
    def teardown(self):
        self.session.close()
    #查询课程成功
    def test01_select_course_success(self):
        self.course_api = CourseAPI(with_token=True)
        response = self.course_api.select_course(test_data="?name=测试开发提升课01")
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
        self.course_api = CourseAPI(with_token=False)
        response = self.course_api.select_course(test_data="?name=00")
        print(response.json())
        # 断言
        # 状态码200
        assert 200 == response.status_code
        # 包含失败
        assert "失败" in response.text
        # json中code值为401
        assert 401 == response.json().get("code")
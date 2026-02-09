import requests
from api.login import LoginAPI
from api.course import CourseAPI
import pytest
import json

class TestDeleteCourseAPI:
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
        TestDeleteCourseAPI.TOKEN = res_login.json().get("token")
    #后置条件
    def teardown(self):
        pass
    #课程删除成功
    def test01_delete_course_success(self,):
        res_course = self.api_course.delete_course(course_id=110,token=TestDeleteCourseAPI.TOKEN)
        print(res_course.json())
        #断言
        #状态码200
        assert 200 == res_course.status_code
        #包含成功
        assert "成功" in res_course.text
        #json中code值为200
        assert 200 == res_course.json().get("code")

    #课程删除失败（课程id不存在）
    def test02_delete_course_success(self,):
        res_course = self.api_course.delete_course(course_id=122222,token=TestDeleteCourseAPI.TOKEN)
        print(res_course.json())
        #断言
        #状态码200
        assert 200 == res_course.status_code
        #包含失败
        assert "失败" in res_course.text
        #json中code值为500
        assert 500 == res_course.json().get("code")

    #课程删除失败（未登录）
    def test03_delete_course_fail(self,):
        res_course = self.api_course.delete_course(course_id=110,token="xxx")
        print(res_course.json())
        #断言
        #状态码200
        assert 200 == res_course.status_code
        #包含失败
        assert "失败" in res_course.text
        #json中code值为401
        assert 401 == res_course.json().get("code")
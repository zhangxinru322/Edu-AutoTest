import requests
from api.login import LoginAPI
from api.course import CourseAPI
import pytest
import json

class TestDeleteCourseAPI:
    #前置条件
    def setup_method(self):
        pass
    #后置条件
    def teardown(self):
        self.session.close()
    #课程删除成功
    def test01_delete_course_success(self):
        self.course_api = CourseAPI(with_token=True)
        res_course = self.course_api.delete_course(course_id=110)
        print(res_course.json())
        #断言
        #状态码200
        assert 200 == res_course.status_code
        #包含成功
        assert "成功" in res_course.text
        #json中code值为200
        assert 200 == res_course.json().get("code")

    #课程删除失败（课程id不存在）
    def test02_delete_course_success(self):
        self.course_api = CourseAPI(with_token=True)
        res_course = self.course_api.delete_course(course_id=122222)
        print(res_course.json())
        #断言
        #状态码200
        assert 200 == res_course.status_code
        #包含失败
        assert "失败" in res_course.text
        #json中code值为500
        assert 500 == res_course.json().get("code")

    #课程删除失败（未登录）
    def test03_delete_course_fail(self):
        self.course_api = CourseAPI(with_token=False)
        res_course = self.course_api.delete_course(course_id=110)
        print(res_course.json())
        #断言
        #状态码200
        assert 200 == res_course.status_code
        #包含失败
        assert "失败" in res_course.text
        #json中code值为401
        assert 401 == res_course.json().get("code")
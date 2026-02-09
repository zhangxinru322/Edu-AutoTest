import requests
from api.login import LoginAPI
from api.course import CourseAPI
import pytest
import json
import config

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
            subject = case_data.get("subject")
            price = case_data.get("price")
            applicablePerson = case_data.get("applicablePerson")
            status = case_data.get("status")
            message = case_data.get("message")
            code = case_data.get("code")
            #追加到空列表
            test_data.append((name,subject,price,applicablePerson,status,message,code))
    return test_data

class TestAddCourseAPI:
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
        TestAddCourseAPI.TOKEN = res_login.json().get("token")
    #后置条件
    def teardown(self):
        pass
    #添加课程成功
    @pytest.mark.parametrize("name,subject,price,applicablePerson,status,message,code",
                             build_data(json_file=config.BASE_PATH + "/data/course.json", case_type="success"))
    def test01_add_course_success(self,name,subject,price,applicablePerson,status,message,code):
        add_data = {
            "name": name,
            "subject": subject,
            "price": price,
            "applicablePerson":applicablePerson
        }
        res_course = self.api_course.add_course(test_data=add_data,token=TestAddCourseAPI.TOKEN)
        print(res_course.json())
        #断言
        #状态码200
        assert status == res_course.status_code
        #包含成功
        assert message in res_course.text
        #json中code值为200
        assert code == res_course.json().get("code")
    #添加课程失败（未登录）
    @pytest.mark.parametrize("name,subject,price,applicablePerson,status,message,code",
                             build_data(json_file=config.BASE_PATH + "/data/course.json", case_type="fail"))
    def test02_add_course_fail(self,name,subject,price,applicablePerson,status,message,code):
        add_data = {
            "name": name,
            "subject":subject,
            "price": price,
            "applicablePerson": applicablePerson
        }
        res_course = self.api_course.add_course(test_data=add_data,token="xxx")
        print(res_course.json())
        # 断言
        # 状态码200
        assert status == res_course.status_code
        # 包含失败
        assert message in res_course.text
        # json中code值为401
        assert code == res_course.json().get("code")
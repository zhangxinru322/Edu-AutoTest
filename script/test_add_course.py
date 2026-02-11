import requests
from api.course import CourseAPI
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
    #前置条件
    def setup_method(self):
        self.session = requests.Session()
    #后置条件
    def teardown(self):
        self.session.close()
    #添加课程成功
    @pytest.mark.parametrize("name,subject,price,applicablePerson,status,message,code",
                             build_data(json_file=BASE_PATH + "/data/course.json", case_type="success"))
    def test01_add_course_success(self,name,subject,price,applicablePerson,status,message,code):
        self.course_api = CourseAPI(with_token=True)
        add_data = {
            "name": name,
            "subject": subject,
            "price": price,
            "applicablePerson":applicablePerson
        }
        res_course = self.course_api.add_course(test_data=add_data)
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
                             build_data(json_file=BASE_PATH + "/data/course.json", case_type="fail"))
    def test02_add_course_fail(self,name,subject,price,applicablePerson,status,message,code):
        self.course_api = CourseAPI(with_token=False)
        add_data = {
            "name": name,
            "subject":subject,
            "price": price,
            "applicablePerson": applicablePerson
        }
        res_course = self.course_api.add_course(test_data=add_data)
        print(res_course.json())
        # 断言
        # 状态码200
        assert status == res_course.status_code
        # 包含失败
        assert message in res_course.text
        # json中code值为401
        assert code == res_course.json().get("code")
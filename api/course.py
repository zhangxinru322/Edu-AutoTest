#课程接口文档封装
import requests
import config

class CourseAPI:
    #初始化
    def __init__(self):
        self.url_add_course=config.BASE_URL + "/api/clues/course"
        self.url_select_course = config.BASE_URL + "/api/clues/course/list"

    #添加课程
    def add_course(self,test_data,token):
        return requests.post(url=self.url_add_course,headers={"Authorization":token},json=test_data,verify=False)
    #查询课程列表
    def select_course(self,test_data,token):
        return requests.get(url=self.url_select_course + f"/{test_data}",headers={"Authorization":token},json=test_data,verify=False)
    def update_course(self,test_data,token):
        return requests.put(url=self.url_add_course,headers={"Authorization":token},json=test_data,verify=False)
    #删除课程
    def delete_course(self,course_id,token):
        return requests.delete(url=self.url_add_course + f"/{course_id}",headers={"Authorization":token},verify=False)
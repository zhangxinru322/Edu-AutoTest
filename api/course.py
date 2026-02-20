import requests
from api.login import LoginAPI
from config.config import BASE_URL, HEADERS

class CourseAPI:
    def __init__(self, with_token=True):
        #只在这里创建一次session，后续课程接口复用此会话
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        print(f"CourseAPI.__init__ session ID: {id(self.session)}")

        self.url_add_course = BASE_URL + "/api/clues/course"
        self.url_select_course = BASE_URL + "/api/clues/course/list"

        if with_token:
            login_api = LoginAPI()
            #调用登录方法：传入当前session（保证登录和课程接口用同一个会话），获取token
            token = login_api.get_token(test_data=None, session=self.session)
            print(f"CourseAPI 拿到token后的session ID: {id(self.session)}")
            #若拿到token，把token加到session的请求头
            if token:
                self.session.headers["Authorization"] = f"Bearer {token}"

    def add_course(self, test_data):
        print(f"CourseAPI.add_course session ID: {id(self.session)}")
        return self.session.post(
            url=self.url_add_course,
            json=test_data,
            verify=False
        )

    def select_course(self, test_data):
        print(f"CourseAPI.select_course session ID: {id(self.session)}")
        return self.session.get(
            url=self.url_select_course + f"/{test_data}",
            json=test_data,
            verify=False
        )

    def update_course(self, test_data):
        print(f"CourseAPI.update_course session ID: {id(self.session)}")
        return self.session.put(
            url=self.url_add_course,
            json=test_data,
            verify=False
        )

    def delete_course(self, course_id):
        print(f"CourseAPI.delete_course session ID: {id(self.session)}")
        return self.session.delete(
            url=self.url_add_course + f"/{course_id}",
            verify=False
        )
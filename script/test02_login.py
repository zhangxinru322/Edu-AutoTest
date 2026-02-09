import requests

url="https://kdtx-test.itheima.net/api/login"
header={
    "Content-Type":"application/json;charset=UTF-8"
}
login_data={
    "username":"admin",
    "password":"HM_2023_test",
    "code":"2",
    "uuid":"0395574269d94bb9b771dc59886b496f"
}
response=requests.post(url=url,headers=header,json=login_data,verify=False)
print(response.status_code)
print(response.json())
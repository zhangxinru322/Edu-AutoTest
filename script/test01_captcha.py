import requests

response=requests.get(url="https://kdtx-test.itheima.net/api/captchaImage",verify=False)

print(response.status_code)
print(response.text)
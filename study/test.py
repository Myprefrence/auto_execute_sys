import requests

response = requests.get(url='https://disconfdev.jiuliyuntech.com/api/web/config/list?appId=201&envId=24&version=1.0.0&')
print(response.text)
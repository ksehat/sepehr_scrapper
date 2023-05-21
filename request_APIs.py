import requests
import json


def call_sepehr(data):
    r = requests.post(url='http://192.168.40.155:3000', data=data)
    # df = pd.DataFrame(columns=r.json()['columns'], data=r.json()['data'])
    return r


def call_input_setting_db(token):
    r = requests.get(
        url='http://192.168.115.10:8081/api/RouteMonitoring/GetAllRouteMonitoringDetail',
        headers={'Authorization': f'Bearer {token}'}
    )
    return r


def call_login_token():
    dict1 = {
        "username": "k.sehat",
        "password": "Ks@123456",
        "applicationType": 961,
        "iP": "1365"
    }
    r = requests.post(url='http://192.168.115.10:8081/api/Authentication/RequestToken',
                      json=dict1,
                      )
    token = json.loads(r.text)['token']
    expire_date = json.loads(r.text)['expires']
    return token, expire_date




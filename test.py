import pandas as pd
import json
import requests

url = "http://192.168.115.17:3000/call_from_backend_to_scrap"

payload = json.dumps({
  "Orig": "THR",
  "Dest": "MHD",
  "date": "2023-12-06",
  "id": 1450124852
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

data = pd.DataFrame(json.loads(json.loads(response.content)['data']))
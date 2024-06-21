import requests

url="https://upcar.up.gov.in/en/page/advisory"
try:
    response=requests.get(url)
    print("Success",response.status_code)
except Exception as e:
    print("Failed", response.status_code, e)


import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

url = os.getenv('REQUEST_URL', 'https://upcar.up.gov.in/en/page/advisory')
print(f"URL to request: {url}")

session = requests.Session()
retry = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

try:
    print("Sending request...")
    response = session.get(url, timeout=20) 
    print(f"Response received with status code: {response.status_code}")
    if response.ok:
        print("Request successful!")
    else:
        print("Request failed with status code:", response.status_code)
except requests.exceptions.ConnectTimeout as e:
    print("Connection timed out. Please check the server or your network connection.")
except requests.exceptions.HTTPError as e:
    print("HTTP error occurred:", e)
except requests.exceptions.ReadTimeout as e:
    print("Read timed out. The server did not send any data in the allotted amount of time.")
except requests.exceptions.RequestException as e:
    print("An error occurred during the request:", e)

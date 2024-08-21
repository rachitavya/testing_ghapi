import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

url = os.getenv('REQUEST_URL', 'https://upcar.up.gov.in/en/page/advisory')
print(f"URL to request: {url}")

try:
    print("here0")
    response = requests.get(url, timeout=30)
    print("here")
    soup = BeautifulSoup(response.text, 'html.parser')

    download_link = soup.find('a', class_='btn btn-success btn-xs external')['href']
    uploading_date = soup.find('span', class_='pdf-details').find_all('strong')[-1].next_sibling.strip()
    data={
        "download_url":download_link,
        "date":uploading_date
    }

    print(data)

except Exception as e:
    print(str(e))
    print("LOL")


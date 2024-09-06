import requests
from bs4 import BeautifulSoup
import os
url=os.environ.get("URL")
try:
    response = requests.get(url)
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
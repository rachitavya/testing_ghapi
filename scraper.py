import os
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Set the URL from an environment variable or use the default URL
# url = os.getenv('REQUEST_URL', 'https://upcar.up.gov.in/en/page/advisory')
# print(f"URL to request: {url}")

# # Function to create a session with retries
# def create_session():
#     session = requests.Session()
#     retry = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
#     adapter = HTTPAdapter(max_retries=retry)
#     session.mount('http://', adapter)
#     session.mount('https://', adapter)
#     return session

# # Imitate a browser by setting headers
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
# }

# try:
#     print("Fetching the data...")
    
#     # Create a session and fetch the URL with a timeout
#     session = create_session()
#     response = session.get(url, headers=headers, timeout=30)
    
#     # Parse the HTML content with BeautifulSoup
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Find the download link and uploading date
#     download_link = soup.find('a', class_='btn btn-success btn-xs external')['href']
#     uploading_date = soup.find('span', class_='pdf-details').find_all('strong')[-1].next_sibling.strip()
    
#     # Store the data in a dictionary
#     data = {
#         "download_url": download_link,
#         "date": uploading_date
#     }

#     print(data)

# except Exception as e:
#     print(f"An error occurred: {str(e)}")
#     print("LOL")


url = 'https://ouat.ac.in/quick-links/agro-advisory-services/'
rename_districts = {
    'angul': 'anugul',
    'balasore': 'baleshwar',
    'boudh': 'baudh',
    'deogarh': 'debagarh',
    'keonjhar': 'kendujhar',
    'mayurbhanjha': 'mayurbhanj',
    'nabarangpur': 'nabarangapur',
    'sonepur': 'subarnapur'
}    
try:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = []
    districts = soup.find_all('div', class_='hide1')
    for district in districts:
        district_name = district.get('id')[:-1]
        if district_name in rename_districts.keys():
            district_name=rename_districts[district_name]
        data_dict = {'district_name': district_name}
        table = district.find('table').find('tbody')
        if len(table.select('tr')) > 0:
            rows = table.select('tr')[0]
        else:
            continue
        columns = rows.find_all('td')
        date = columns[1].text.strip()
        data_dict['date'] = date
        english_link = columns[2].find('a')['href']
        odia_link = columns[3].find('a')['href']
        link_dict = {'english': english_link, 'odia': odia_link}
        data_dict['link'] = link_dict
        data.append(data_dict)
    print(data)

except Exception  as e:
    print("Error:",e)
    
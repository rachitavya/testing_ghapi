import json
import logging
import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO)


def scraper():
    url = "https://ouat.ac.in/quick-links/agro-advisory-services/"
    rename_districts = {
        "angul": "anugul",
        "balasore": "baleshwar",
        "boudh": "baudh",
        "deogarh": "debagarh",
        "keonjhar": "kendujhar",
        "mayurbhanjha": "mayurbhanj",
        "nabarangpur": "nabarangapur",
        "sonepur": "subarnapur",
    }
    try:
        # Perform the request and log headers
        headers={'User-Agent': 'python-requests/2.31.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")

        data = []
        districts = soup.find_all("div", class_="hide1")
        for district in districts:
            district_name = district.get("id")[:-1]
            if district_name in rename_districts.keys():
                district_name = rename_districts[district_name]
            data_dict = {"district_name": district_name}
            table = district.find("table").find("tbody")
            if len(table.select("tr")) > 0:
                rows = table.select("tr")[0]
            else:
                continue
            columns = rows.find_all("td")
            date = columns[1].text.strip()
            data_dict["date"] = date
            english_link = columns[2].find("a")["href"]
            odia_link = columns[3].find("a")["href"]
            link_dict = {"english": english_link, "odia": odia_link}
            data_dict["link"] = link_dict
            data.append(data_dict)

        return {"statusCode": 200, "body": json.dumps(data)}

    except Exception as e:
        logging.error(f"Error scraping website: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}


print(scraper())

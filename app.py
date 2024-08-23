from playwright.sync_api import sync_playwright

def scraper_new():
    try:
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=True)
            page = browser.new_page()
            page.goto('https://ouat.ac.in/quick-links/agro-advisory-services/')
            content = page.content()
            # Assuming BeautifulSoup for HTML parsing
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')

            data = []
            districts = soup.find_all('div', class_='hide1')
            for district in districts:
                district_name = district.get('id')[:-1]
                if district_name in rename_districts.keys():
                    district_name = rename_districts[district_name]
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

    except Exception as e:
        print("Error", str(e))

scraper_new()
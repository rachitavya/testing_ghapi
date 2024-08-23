from selenium import webdriver
from bs4 import BeautifulSoup

# Assuming you have a dictionary for renaming districts
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

def scraper_new():
    try:
        # Set up Firefox options
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")  # Run in headless mode for GitHub Actions

        # Initialize WebDriver
        driver = webdriver.Firefox(options=options)

        # Fetch the webpage
        driver.get('https://ouat.ac.in/quick-links/agro-advisory-services/')

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

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

        # Print the data
        print(data)

    except Exception as e:
        print("Error:", str(e))
    finally:
        # Close the browser
        driver.quit()

# Run the scraper
scraper_new()

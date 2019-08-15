from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import unicodecsv as csv

# Function for opening the WebDriver, scrolling for max page view, and then capturing the html
def FFwebdriver(driver):
    # Give the browser time to load the page
    time.sleep(10)
    pause = 3

    # Empty Page? If so, bounce.
    try:
        lastHeight = driver.execute_script("return document.body.scrollHeight")
    except:
        return None
    
    # Scroll to the bottom, and hit more a bunch to get max results
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)

        # If you can't find the 'more' button, break to grab the html
        try:
            driver.find_element_by_class_name('more').click()
        except:
            break
        
        # Load new page and then reorient
        time.sleep(pause)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight

    time.sleep(pause)
    htmlResults = driver.page_source

    return htmlResults


# Function for parsing and scraping the HTML for the key attributes
def scraping(html, company_list):
    soup = BeautifulSoup(html, 'html.parser')
    raw_companies = soup.find_all('div', class_='base startup')

    #Iterate and pull out the key attributes
    for targetsoup in raw_companies:
        # Company Name
        company_name = targetsoup.find_all("a", class_="startup-link")[1].get_text().strip('\n')

        try: # AngelList Link
            angellist_website = targetsoup.find("a", class_="startup-link").get('href').strip('\n')
        except AttributeError:
            angellist_website = "Empty section for this company"

        try: # Company Tagline
            tagline = targetsoup.find("div", class_="pitch").get_text().strip('\n')
        except AttributeError:
            tagline = "Empty section for this company"

        company_dict = {'name': company_name, 
                        'AngelList_website': angellist_website,
                        'tagline': tagline}
        company_list.append(company_dict)

    return company_list


def exportingToCSV(company_list, start, stop):
    csv_name = 'angel-co-' + str(start) + '-' + str(stop) + '.csv'
    with open(csv_name, 'wb') as outfile:
        writer = csv.DictWriter(outfile, company_list[0].keys())
        writer.writeheader()
        writer.writerows(company_list)


# Requires geckodriver for FF or similar driver for other browsers
driver = webdriver.Firefox(executable_path='C:/Users/Zero/Downloads/geckodriver-v0.24.0-win64/geckodriver.exe')

stages = ['Seed', 'Series+A', 'Series+B', 'Series+C', 'Acquired']
root_url = 'https://angel.co/companies?signal[min]=5&signal[max]=10&stage[]='
company_list = list()

# Change to narrow the search, funds raised ranges require different
# step amounts so the scraper doesn't miss too many companies
start = 1000000
stop = 100000000
incr = 1000000

for stage in stages:
    for i in range(start, stop, incr):
        url = root_url + stage + '&raised[min]=' + str(i) + '&raised[max]=' + str(i+incr)
        
        # Navigate to the right page for scraping
        driver.get(url)
        html = FFwebdriver(driver)

        # Parse the html
        if html is not None:
            company_list = scraping(html, company_list)
        
        # Save regularly
        if i % (incr*10) == 0:
            print(i)
            exportingToCSV(company_list, start, stop)
    print(stage)
    exportingToCSV(company_list, start, stop)
driver.quit()
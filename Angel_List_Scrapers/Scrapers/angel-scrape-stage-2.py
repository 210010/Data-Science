from selenium import webdriver
import pandas as pd
import datetime
import time
import bs4


'''
This script requires an auto-switching VPN to work properly. If you run without regularly switching IP addresses
Angel List detects the scraper and throws up a captcha. Recommend Hide My Ass v2 or similar VPN.
'''

# Function for opening the WebDriver, scrolling for max page view, and then capturing the html
def FFwebdriver(driver, url):
    driver.get(url)
    time.sleep(15)

    # One format of the company pages has a 'Read more' button that must be clicked to reveal all
    # relevant html, the other format has a button but the text is still visible in html thus passing
    try:
        driver.find_element_by_xpath("//*[text()='Read more']") .click()
    except:
        pass

    time.sleep(5)
    htmlResults = driver.page_source

    return htmlResults


def csv_scrape(csv):
    descriptions = list()

    # Initialize the webdriver
    driver=webdriver.Firefox(executable_path='C:/Users/Zero/Downloads/geckodriver-v0.24.0-win64/geckodriver.exe')
    
    # Turn raw csv from github into dataframe for ease
    df = pd.read_csv(csv)
    
    start = datetime.datetime.now()
    # Conditionally searches angellist for products with taglines and extracts the html
    for i in range(len(df)):
        desc = 'Empty'
        if df['tagline'][i] != "Empty section for this company":
            url = df.AngelList_website[i]
            html = FFwebdriver(driver, url)
            soup = bs4.BeautifulSoup(html, 'html.parser')

            # Attempt to parse the html, pages have two formats for description plus a no description format
            try:
                desc = soup.find(class_="component_bc35d").get_text().strip()
            except:
                try:
                    desc = soup.find("div", class_="product_desc").get_text().strip()
                except:
                    desc = 'Empty'
            descriptions.append(desc)
        
    # Create a new column in the DataFrame
    df['descriptions'] = descriptions
    return df


# Run the scraper and then export to CSV
# Change the CSV name below to 'angel-co-desc-' + funding range of the seed csv + '.csv'
df = csv_scrape('https://raw.githubusercontent.com/veritaem/DS-Sprint-01-Dealing-With-Data/master/angel-co-1000000-100000000.csv')
df.to_csv('angel-co-desc-1000000-100000000.csv')
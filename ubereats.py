from selenium import webdriver
import scrape_restaurants

url_prefix = 'https://www.ubereats.com/tw/category/'
cities = ['taipei']

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome('./chromedriver.exe', options=chrome_options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => false
        })
    """
    })

for city in cities:
    scrape_restaurants.getRestaurants(driver, url_prefix+city, city)
    scrape_restaurants.getRestaurantInfo(driver, city)

stop = input()
driver.quit()
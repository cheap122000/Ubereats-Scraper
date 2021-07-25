import string
from selenium import webdriver
import json
import os
from urllib.parse import unquote
import re
import time
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys

def getRestaurants(driver: webdriver.Chrome, url: str, city: str):
    driver.get(url)

    categories_zh = driver.find_element_by_xpath('/html/body/div/div/main/div[2]/div[3]').text.replace(" ", "-").lower().splitlines()
    categories_link = [x.get_attribute('href') for x in driver.find_element_by_xpath('/html/body/div/div/main/div[2]/div[3]').find_elements_by_css_selector('a')]

    categories = []
    for i in range(len(categories_zh)):
        categories.append({"category_name": categories_zh[i], "category_link": categories_link[i]})

    # record the categories
    if not os.path.isdir("./src"):
        os.mkdir("./src")
    with open('./src/categories.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(categories, ensure_ascii=False))

    for category in categories:
        try:
            driver.get(category['category_link'])
            urls = [x.get_attribute('href') for x in driver.find_element_by_xpath("/html/body/div/div/main/div[5]").find_elements_by_tag_name("a")]
            if not os.path.isdir('./src/categories'):
                os.mkdir('./src/categories')
            if not os.path.isdir(f"./src/categories/{city}"):
                os.mkdir(f"./src/categories/{city}")
            with open(f"./src/categories/{city}/{category['category_name']}.json", 'w', encoding='utf8') as f:
                f.write(json.dumps(urls, ensure_ascii=False))
        except:
            print(f"Scrapped failed in category: {category}")

def getRestaurantInfo(driver: webdriver.Chrome, city: str):
    address = '台北市大安區仁愛路四段345巷4弄'
    for city in os.listdir('./src/categories'):
        for category in os.listdir(f'./src/categories/{city}'):
            with open(f'./src/categories/{city}/{category}', 'r', encoding='utf8') as f:
                urls = json.loads(f.read())
                mem = None
            for url in urls:
                # print(url)
                if mem != None:
                    if url.find(mem) != -1:
                        continue
                driver.get(url)
                try:
                    driver.find_element_by_id('location-typeahead-location-manager-input').send_keys(address)
                    time.sleep(3)
                    driver.find_element_by_id('location-typeahead-location-manager-input').send_keys(Keys.ENTER)
                    time.sleep(3)
                except:
                    pass
                infoUrl = driver.find_element_by_xpath('/html/body/div/div/main/div[4]/div/div/p/a').get_attribute('href')
                storeName, storeUUID = parseRestaurantInfo('uuid', infoUrl)
                longitude, latitude = parseRestaurantInfo('geo', driver.page_source)
                categoryToShow = category.replace('.json', '')
                print(f'{city}, {categoryToShow}, {storeName}, {storeUUID}, {longitude}, {latitude}')
                mem = url

                # break
            # break

def parseRestaurantInfo(target: str, content: str):
    if target == 'uuid':
        content = unquote(unquote(unquote(content)))
        matches = re.findall('{[\w\W]+}', content)
        if len(matches) > 0:
            storeName = json.loads(matches[0])['storeSlug']
            storeUUID = json.loads(matches[0])['storeUuid']
        return storeName, storeUUID
    elif target == 'geo':
        matches = re.findall(r'<script type="application\/ld\+json">{"@context":[\w\W]+}]}<\/script>', content)
        jsonBody = json.loads(unquote(matches[0].replace('\\u002F', '/')).replace(r'<script type="application/ld+json">', '').replace(r'</script>', '').replace('\n', ''))
        longitude = jsonBody['geo']['longitude']
        latitude = jsonBody['geo']['latitude']
        return longitude, latitude




if __name__ == "__main__":
    parseRestaurantInfo('uuid', 'https://www.ubereats.com/tw/store/watsons%E5%B1%88%E8%87%A3%E6%B0%8F-%E7%B5%B1%E9%A0%98%E9%96%80%E5%B8%82-s0031/CNukTq_KQcW3lXTs8CIYdg?mod=storeLocationHours&modctx=%257B%2522storeSlug%2522%253A%2522watsons%2525E5%2525B1%252588%2525E8%252587%2525A3%2525E6%2525B0%25258F-%2525E7%2525B5%2525B1%2525E9%2525A0%252598%2525E9%252596%252580%2525E5%2525B8%252582-s0031%2522%252C%2522storeUuid%2522%253A%252208dba44e-afca-41c5-b795-74ecf0221876%2522%252C%2522sectionUuid%2522%253A%2522%2522%257D&ps=1')
    t = """
    <script type="application/ld+json">{"@context":"http:\u002F\u002Fschema.org","@type":"Restaurant","@id":"https:\u002F\u002Fwww.ubereats.com\u002Ftw\u002Fstore\u002Fwatsons%E5%B1%88%E8%87%A3%E6%B0%8F-%E7%B5%B1%E9%A0%98%E9%96%80%E5%B8%82-s0031\u002FCNukTq_KQcW3lXTs8CIYdg","name":"Watsons屈臣氏 統領門市 S0031","servesCuisine":["生鮮雜貨","美妝母嬰"],"priceRange":"$","image":["https:\u002F\u002Fd1ralsognjng37.cloudfront.net\u002F63872209-adb2-45e4-a0cf-ce578ba6b4d6.jpeg","https:\u002F\u002Fd1ralsognjng37.cloudfront.net\u002Fa70e6dde-6733-4fe7-8a77-a47b2084f12e.jpeg","https:\u002F\u002Fd1ralsognjng37.cloudfront.net\u002F204f888a-bd7c-48bc-9d1e-4f2909329766.jpeg","https:\u002F\u002Fd1ralsognjng37.cloudfront.net\u002Fe0756981-8f6e-48fa-8566-a136f52fae50.jpeg","https:\u002F\u002Fd1ralsognjng37.cloudfront.net\u002F9b2dc927-2297-4745-a618-7a82af9c6d58.jpeg","https:\u002F\u002Fd1ralsognjng37.cloudfront.net\u002F0e5e4dc6-1727-413e-bf69-377ec842249a.jpeg"],"potentialAction":{"@type":"OrderAction","target":{"@type":"EntryPoint","urlTemplate":"https:\u002F\u002Fwww.ubereats.com\u002Ftw\u002Fstore\u002Fwatsons%E5%B1%88%E8%87%A3%E6%B0%8F-%E7%B5%B1%E9%A0%98%E9%96%80%E5%B8%82-s0031\u002FCNukTq_KQcW3lXTs8CIYdg?utm_campaign=order-action&amp;amp;utm_medium=organic","inLanguage":"中文","actionPlatform":["http:\u002F\u002Fschema.org\u002FDesktopWebPlatform","http:\u002F\u002Fschema.org\u002FMobileWebPlatform"]},"deliveryMethod":["http:\u002F\u002Fpurl.org\u002Fgoodrelations\u002Fv1#DeliveryModeOwnFleet"]},"address":{"@type":"PostalAddress","addressLocality":"Taipei","addressRegion":"","postalCode":"106","addressCountry":"TW","streetAddress":"台北市大安區忠孝東路四段209號"},"geo":{"@type":"GeoCoordinates","latitude":25.04172,"longitude":121.55201},"telephone":"+886227788160","aggregateRating":{"@type":"AggregateRating","ratingValue":4.8,"reviewCount":"146"},"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"10:0","closes":"21:30"}]}</script>
    """
    print(t.encode().decode('utf8', 'ignore'))
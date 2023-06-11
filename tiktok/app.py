# import requests
# from list import country_info
# import time

# header = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#     "Referer": "https://ads.tiktok.com/business/creativecenter/inspiration/popular/music/pad/en",
#     "Accept": "application/json, text/plain, */*",
#     "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
#     "User-Sign": "60644e3bc5adcbb9",
#     "Web-Id": "7201805665697744385",
#     "anonymous-user-id": '7726c546122c4f41857f3207f2a690cf',
#     "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
#     "sec-ch-ua-platform": "macOS",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "sec-ch-ua-mobile": "?0",
#     "lang": "en",
#     "timestamp": "1686457663",
#     "authority": "ads.tiktok.com",
# }




# def get_options():
#     url = "https://ads.tiktok.com/creative_radar_api/v1/popular_trend/sound/filters"
#     response = requests.get(url, headers=header, params={
#         "rank_type": "popular"
#     })
#     print(response.text, response.status_code)
#     return response.json()


# def get_trends():
#     url = "https://ads.tiktok.com/creative_radar_api/v1/popular_trend/sound/rank_list"
#     # url = "http://localhost:8081/creative_radar_api/v1/popular_trend/sound/rank_list"
#     r = requests.get(url, headers=header, params={
#         "period": "7",
#         "page": "1",
#         "limit": "3",
#         "country_code": "US",
#         "new_on_board": "false",
#         "commercial_music": "false",
#         "rank_type": "popular",
#     })
#     return r.json()


# def get_trends_video():
#     print(get_trends())


# if __name__ == "__main__":
#     get_trends_video()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--enable-javascript")

driver = webdriver.Chrome()
driver.implicitly_wait(15)
driver.get("https://ads.tiktok.com/business/creativecenter/inspiration/popular/music/pc/en")
elem = driver.find_element(By.XPATH, '//*[@id="ccContentContainer"]/div[2]/div/div[2]/div[2]/div')
print(elem)
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()

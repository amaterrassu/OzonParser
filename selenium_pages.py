from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import json


class UseSelenium:
    def __init__(self, url: str, MAX_PAGE: int):
        self.url = url
        self.jsonlink = ''
        self.MAX_PAGE = MAX_PAGE
        chrm_options = Options()
        chrm_caps = webdriver.DesiredCapabilities.CHROME.copy()
        chrm_options.headless = True
        chrm_caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-accelerated-mjpeg-decode')
        chrome_options.add_argument('--disable-accelerated-2d-canvas')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument('--disable-gpu-rasterization')
        self.navigator = None
        self.driver = uc.Chrome(options=chrome_options, desired_capabilities=chrm_caps)

    def save_page(self):
        i = 1
        while i <= self.MAX_PAGE:
            self.jsonlink = f'page_' + str(i) + '.json'
            if i == 1:
                try:
                    self.driver.get(self.url)
                    time.sleep(3)
                    self.driver.execute_script("window.scrollTo(5,4000);")
                    time.sleep(5)
                    self.get_links()
                except Exception as ex:
                    print(ex)
                finally:
                    pass
            else:
                url_param = self.url + '?page=' + str(i)
                print(url_param)
                try:
                    self.driver.get(self.url)
                    time.sleep(3)
                    self.driver.execute_script("window.scrollTo(5,4000);")
                    time.sleep(5)
                    self.get_links()
                except Exception as ex:
                    print(ex)
                finally:
                    pass
            i += 1

    def get_links(self):
        links = []
        for i in range(1, 37):
            try:
                lnk = self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div/div[{i}]/a').get_attribute('href')
            except Exception as ex:
                print('Failed to get link', ex)
                continue
            meta = self.get_info(lnk)
            meta['link'] = lnk
            links.append(meta)
        links = json.dumps({"products": links})
        with open('/Users/dankulakovich/PycharmProjects/OzonParser/json_links/' + self.jsonlink, 'w', encoding='utf-8') as f:
            f.write(links)

    def get_info(self, link):
        user_price = None
        card_price = None
        price = None
        rating = None
        review = None
        try:
            self.driver.get(link)
            time.sleep(3)
            try:
                user_price = float(self.driver.find_element(By.XPATH, "//*[@class='l9n n9l lo nl8']").text.split()[0].replace(',', '.'))
            except Exception as ex:
                print('Can\'t parse user_price', ex)
            try:
                card_price = float(self.driver.find_element(By.CLASS_NAME, 'n4l').text.split()[0].replace(',', '.'))
            except Exception as ex:
                print('Can\'t parse card_price', ex)
            try:
                price = float(self.driver.find_element(By.CLASS_NAME, 'nl9').text.split()[0].replace(',', '.'))
            except Exception as ex:
                print('Can\'t parse price', ex)
            try:
                rating = float(self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[5]/div/div[1]/div[2]/div/div[1]/div/div[2]/ul/li[1]/div/div/span/span[1]').text.replace(',', '.'))
            except Exception as ex:
                print('Can\'t parse rating', ex)
                rating = 0
            try:
                review = int(self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[3]/div[2]/div/div/div[2]/div/div[1]/div[1]/div/div/div[2]/a/div/div').text.split()[0])
            except Exception as ex:
                print('Can\'t parse review', ex)
                review = 0

        except Exception as ex:
            print(ex, link)
        finally:
            self.driver.execute_script("window.history.go(-1)")
            time.sleep(2)
            print(user_price, card_price, price, rating, review, sep='\n')
        return {
            'user_price': user_price,
            'card_price': card_price,
            'price': price,
            'rating': rating,
            'review': review
        }



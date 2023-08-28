from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import json


class UseSelenium:
    def __init__(self, url: str, filename: str, jsonlink: str):
        self.url = url
        self.filename = filename
        self.jsonlink = jsonlink
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

        try:
            self.driver.get(self.url)
            time.sleep(3)
            self.driver.execute_script("window.scrollTo(5,4000);")
            time.sleep(5)
            self.get_links()
            html = self.driver.page_source
            with open('/Users/dankulakovich/PycharmProjects/OzonParser/pages/' + self.filename, 'w', encoding='utf-8') as f:
                f.write(html)
        except Exception as ex:
            print(ex)
        finally:
            self.driver.close()
            self.driver.quit()

    def get_links(self):
        links = []
        for i in range(1, 37):
            links.append(self.driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div/div[{i}]/a').get_attribute('href'))
        links = json.dumps({"links": links})
        with open('/Users/dankulakovich/PycharmProjects/OzonParser/json_links/' + self.jsonlink, 'w', encoding='utf-8') as f:
            f.write(links)

    def get_info(self, link):
        try:
            self.driver.get(link)
            time.sleep(3)


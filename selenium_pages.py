import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.options import Options


class UseSelenium:
    def __init__(self, url: str, filename: str):
        self.url = url
        self.filename = filename

    def save_page(self):

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
        navigator = None
        driver = uc.Chrome(options=chrome_options, desired_capabilities=chrm_caps)

        try:
            driver.get(self.url)
            time.sleep(3)
            driver.execute_script("window.scrollTo(5,4000);")
            time.sleep(5)
            html = driver.page_source
            with open('/Users/georgezagorsky/build/OzonParser/pages/' + self.filename, 'w', encoding='utf-8') as f:
                f.write(html)
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

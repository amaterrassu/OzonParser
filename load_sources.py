from selenium_pages import UseSelenium

def main():
    url = "https://www.ozon.ru/category/kompasy-11461/"
    MAX_PAGE = 3
    UseSelenium(url, MAX_PAGE).save_page()

if __name__ == '__main__':
    main()
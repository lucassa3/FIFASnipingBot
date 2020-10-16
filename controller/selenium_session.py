from selenium import webdriver


class SeleniumSession:
    def __init__(self, url_name):
        self.url_name = url_name

        self.options = webdriver.ChromeOptions()
        self.options.add_argument("user-data-dir=profile/")
        self.driver = webdriver.Chrome("chromedriver.exe", chrome_options=self.options)

        self.driver.set_page_load_timeout("10")
        self.driver.get(url_name)

    def getWebDriver(self):
        return self.driver

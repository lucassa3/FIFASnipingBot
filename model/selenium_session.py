from selenium import webdriver


class SeleniumSession:
    def __init__(self, url_name):

        self.url_name = url_name

        profile_path = "/profile"

        options = webdriver.ChromeOptions()
        options.add_argument(f"user-data-dir={profile_path}")

        self.driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
        self.driver.set_page_load_timeout("10")
        self.driver.get(url_name)

    def get_web_driver(self):
        return self.driver

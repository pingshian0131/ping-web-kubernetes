import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver


class MySeleniumTests(StaticLiveServerTestCase):
    # fixtures = ["user-data.json"]

    driver = None

    @classmethod
    def setUpClass(cls):
        cls.live_server_url = "http://127.0.0.1:8000/"
        super().setUpClass()
        cls.driver = WebDriver()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_login(self):
        self.driver.get(f"{self.live_server_url}")
        self.driver.find_element(By.XPATH, "//*[@id='navbar']/ul/li[6]/a").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//*[@id='name']").send_keys("test_name")
        time.sleep(0.5)
        self.driver.find_element(By.XPATH, "//*[@id='email']").send_keys("aaa@mail.com")
        time.sleep(0.5)
        self.driver.find_element(By.XPATH, "//*[@id='subject']").send_keys("test_subject")
        time.sleep(0.5)
        self.driver.find_element(By.XPATH, "//*[@id='contact']/div/div[2]/div[2]/form/div[3]/textarea").send_keys("test_message")
        time.sleep(0.5)
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//*[@id='contact']/div/div[2]/div[2]/form/div[5]/button").click()
        time.sleep(5)


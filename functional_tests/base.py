from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver    

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
    	self.browser.quit()
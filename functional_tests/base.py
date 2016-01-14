import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver    


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def get_by_id(self, id):
        return self.browser.find_element_by_id(id)

    def get_by_link_text(self, text):
        return self.browser.find_element_by_link_text(text)

    def get_by_partial(self, text):
        return self.browser.find_element_by_partial_link_text(text);

    def login(self, is_teacher):
        if self.browser.current_url != "http://localhost:8000/login":
            self.browser.get("http://localhost:8000/login")
        time.sleep(0.02)
        if is_teacher:
            self.get_by_id('id_username').send_keys('teacher')
        else:
            self.get_by_id('id_username').send_keys('taccount@mail.bg')
        self.get_by_id('id_password').send_keys('example')
        self.get_by_id('submit').click()

    def logout(self):
        self.get_by_link_text('Log out').click()
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver    


class FunctionalTest(StaticLiveServerTestCase):
    fixtures = ['fixtures/users.json', 'fixtures/courses.json',
        'fixtures/questions.json', 'fixtures/exams.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get('http://localhost:8081')

    def tearDown(self):
        self.browser.quit()

    def get_by_id(self, ID):
        return self.browser.find_element_by_id(ID)

    def get_by_class(self, cls):
        return self.browser.find_element_by_class_name(cls)

    def get_by_tag_name(self, tag):
        return self.browser.find_element_by_tag_name(tag)

    def get_by_link_text(self, text):
        return self.browser.find_element_by_link_text(text)

    def get_by_partial(self, text):
        return self.browser.find_element_by_partial_link_text(text);

    def login(self, is_teacher):
        time.sleep(0.1)
        if is_teacher:
            self.get_by_id('id_username').send_keys('teacher')
        else:
            self.get_by_id('id_username').send_keys('student@test.com')
        self.get_by_id('id_password').send_keys('example')
        self.get_by_id('submit').click()

    def logout(self):
        self.get_by_link_text('Log out').click()
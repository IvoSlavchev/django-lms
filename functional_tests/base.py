from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver    

class FunctionalTest(StaticLiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Chrome()

	def tearDown(self):
		self.browser.quit()

	def login(self, is_teacher):
		if is_teacher:
			self.browser.find_element_by_id('id_username').send_keys('teacher')
		else:
			self.browser.find_element_by_id('id_username').send_keys('taccount@mail.bg')

		self.browser.find_element_by_id('id_password').send_keys('example')
		self.browser.find_element_by_id('id_submit').click()
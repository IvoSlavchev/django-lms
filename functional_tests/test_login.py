from .base import FunctionalTest

class LoginTest(FunctionalTest):

	def signup(self, is_teacher):
		if is_teacher:
			self.browser.find_element_by_id('id_is_teacher').click()
			self.browser.find_element_by_id('id_username').send_keys('example_teacher')
		else:
			self.browser.find_element_by_id('id_username').send_keys('example_student')

		self.browser.find_element_by_id('id_email').send_keys('example@example.com')		
		self.browser.find_element_by_id('id_password1').send_keys('example')
		self.browser.find_element_by_id('id_password2').send_keys('example')
		self.browser.find_element_by_id('id_submit').click()

	def login(self, is_teacher):
		if is_teacher:
			self.browser.find_element_by_id('id_username').send_keys('example_teacher')
		else:
			self.browser.find_element_by_id('id_username').send_keys('example_student')

		self.browser.find_element_by_id('id_password').send_keys('example')
		self.browser.find_element_by_id('id_submit').click()

	def test_home_page(self):
		self.browser.get("http://localhost:8081")
		header = self.browser.find_element_by_tag_name('h3').text
		self.assertEqual(header, 'Welcome to the Django-LMS!')

	def test_signup_and_login(self):
		self.browser.get("http://localhost:8081")

		# Register and login with a teacher account
		self.browser.find_element_by_link_text('Signup').click()
		self.signup(True)
		self.assertEqual(self.browser.current_url, 'http://localhost:8081/')

		self.browser.find_element_by_link_text('Login').click()
		self.login(True)
		self.assertEqual(self.browser.current_url, 'http://localhost:8081/teacher')

		# Logout
		self.browser.find_element_by_link_text('Logout').click()
		self.assertEqual(self.browser.current_url, 'http://localhost:8081/login/')	

		# Register and login with a student account
		self.browser.find_element_by_link_text('Signup').click()
		self.signup(False)
		self.assertEqual(self.browser.current_url, 'http://localhost:8081/')

		self.browser.find_element_by_link_text('Login').click()
		self.login(False)
		self.assertEqual(self.browser.current_url, 'http://localhost:8081/student')
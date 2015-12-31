from .base import FunctionalTest

class AuthenticationTest(FunctionalTest):

	def signup(self, is_teacher):
		if is_teacher:		
			self.browser.find_element_by_id('id_username').send_keys('teacher')
		else:
			self.browser.find_element_by_id('id_username').send_keys('student')

		self.browser.find_element_by_id('id_email').send_keys('taccount@mail.bg')		
		self.browser.find_element_by_id('id_password1').send_keys('example')
		self.browser.find_element_by_id('id_password2').send_keys('example')
		self.browser.find_element_by_id('id_submit').click()

	def test_home_page(self):
		self.browser.get("http://localhost:8081")
		header = self.browser.find_element_by_tag_name('h3').text
		self.assertEqual(header, 'Welcome!')

	def test_signup(self):
		self.browser.get("http://localhost:8081")
		self.browser.find_element_by_link_text('Sign up').click()
		self.signup(True)
		self.assertEqual(self.browser.current_url, 'http://localhost:8081/')

		self.browser.find_element_by_link_text('Sign up').click()
		self.signup(False)

	def test_login(self):	
		self.browser.get("http://localhost:8000")
		self.browser.find_element_by_link_text('Log in').click()
		self.login(True)
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/')
		self.browser.find_element_by_link_text('Log out').click()
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/login')	
		
		self.browser.find_element_by_link_text('Log in').click()
		self.login(False)
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/s')
		self.browser.find_element_by_link_text('Log out').click()
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/login')	
from .base import FunctionalTest

class LoginTest(FunctionalTest):

	def signup(self, is_teacher):
		if is_teacher:
			self.browser.find_element_by_id('id_is_teacher').click()
			self.browser.find_element_by_id('id_username').send_keys('example_teacher')
		else:
			self.browser.find_element_by_id('id_username').send_keys('example_student')

		self.browser.find_element_by_id('id_email').send_keys('taccount@mail.bg')		
		self.browser.find_element_by_id('id_password1').send_keys('example')
		self.browser.find_element_by_id('id_password2').send_keys('example')
		self.browser.find_element_by_id('id_submit').click()

	def login(self, is_teacher):
		if is_teacher:
			self.browser.find_element_by_id('id_username').send_keys('teacher')
		else:
			self.browser.find_element_by_id('id_username').send_keys('student')

		self.browser.find_element_by_id('id_password').send_keys('example')
		self.browser.find_element_by_id('id_submit').click()

	def confirm_email(self):
		self.browser.get("http://mail.bg/auth/login")
		self.browser.maximize_window()
		self.browser.find_element_by_id('imapuser').send_keys('taccount@mail.bg')
		self.browser.find_element_by_id('pass').send_keys('1234password\n')
		self.browser.find_element_by_id('inbox').click()
		self.browser.find_element_by_class_name('mail_table_link').click()
		self.browser.switch_to.frame(frame_reference=self.browser.find_element_by_xpath(
										"//iframe[@id='mail_content_body_frame']"))
		self.browser.find_element_by_tag_name('a').click()
		self.browser.switch_to_window(self.browser.window_handles[1])

	def test_home_page(self):
		self.browser.get("http://localhost:8081")
		header = self.browser.find_element_by_tag_name('h3').text
		self.assertEqual(header, 'Welcome to the Django-LMS!')

	def test_signup_and_confirm_email(self):
		# Sign up as teacher
		self.browser.get("http://localhost:8081")
		self.browser.find_element_by_link_text('Signup').click()
		self.signup(True)
		self.assertEqual(self.browser.current_url, 'http://localhost:8081/')
		self.confirm_email()

		# Sign up as student
		self.browser.get("http://localhost:8081")
		self.browser.find_element_by_link_text('Signup').click()
		self.signup(False)
		self.assertEqual(self.browser.current_url, 'http://localhost:8081/')
		self.confirm_email()

	def test__login(self):	
		# Login as teacher	
		self.browser.get("http://localhost:8081")
		self.browser.find_element_by_link_text('Login').click()
		self.login(True)
		self.assertEqual(self.browser.current_url, 'http://localhost:8081/teacher')

		# Logout
		self.browser.find_element_by_link_text('Logout').click()
		self.assertEqual(self.browser.current_url, 'http://localhost:8081/login/')	

		# Login as student
		self.browser.find_element_by_link_text('Login').click()
		self.login(False)
		self.assertEqual(self.browser.current_url, 'http://localhost:8081/student')
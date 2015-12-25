from .base import FunctionalTest

class LoginTest(FunctionalTest):

	def signup(self, is_teacher):
		if is_teacher:		
			self.browser.find_element_by_id('id_username').send_keys('teacher')
		else:
			self.browser.find_element_by_id('id_username').send_keys('student')

		self.browser.find_element_by_id('id_email').send_keys('taccount@mail.bg')		
		self.browser.find_element_by_id('id_password1').send_keys('example')
		self.browser.find_element_by_id('id_password2').send_keys('example')
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
		self.assertEqual(header, 'Welcome!')

	def test_signup(self):
		# Sign up as teacher
		self.browser.get("http://localhost:8081")
		self.browser.find_element_by_link_text('Sign up').click()
		self.signup(True)
		self.assertEqual(self.browser.current_url, 'http://localhost:8081/')
		#self.confirm_email()

		# Sign up as student
		self.browser.find_element_by_link_text('Sign up').click()
		self.signup(False)
		self.assertEqual(self.browser.current_url, 'http://localhost:8081/')
		#self.confirm_email()

	def test__login(self):	
		# Logging into the real server as to not have to create new users		
		self.browser.get("http://localhost:8000")
		self.browser.find_element_by_link_text('Log in').click()
		# Login as teacher	
		self.login(True)
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/teachers/')

		# Logout
		self.browser.find_element_by_link_text('Log out').click()
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/login')	
		
		self.browser.find_element_by_link_text('Log in').click()
		# Login as student
		self.login(False)
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/students/')
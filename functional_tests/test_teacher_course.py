from .base import FunctionalTest

class TeacherCourseTest(FunctionalTest):

	def test_course_creation_and_listing(self):
		self.browser.get("http://localhost:8000")
		self.browser.find_element_by_link_text('Log in').click()
		self.login(True)
		self.browser.find_element_by_link_text('Create new course').click()
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/teachers/create/')

		self.browser.find_element_by_id('id_name').send_keys('Example course')		
		self.browser.find_element_by_id('id_description').send_keys('Example description')
		self.browser.find_element_by_id('id_submit').click()
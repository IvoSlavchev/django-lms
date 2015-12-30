from .base import FunctionalTest

class CourseTest(FunctionalTest):

	def test_course_creation_editing_and_viewing(self):
		self.browser.get("http://localhost:8000")
		self.browser.find_element_by_link_text('Log in').click()
		self.login(True)
		self.browser.find_element_by_link_text('Create new course').click()
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/create')

		self.browser.find_element_by_id('id_name').send_keys('Example course')		
		self.browser.find_element_by_id('id_description').send_keys('Example description')		
		self.browser.find_element_by_id('id_submit').click()
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/')

		self.browser.find_element_by_partial_link_text('Example course').click()
		self.browser.find_element_by_link_text('Edit participants').click()
		self.browser.find_element_by_id('id_participants_0').click()
		self.browser.find_element_by_id('id_submit').click()
		self.browser.find_element_by_id('id_description').clear()
		self.browser.find_element_by_id('id_description').send_keys('Changed')
		self.browser.find_element_by_id('id_submit').click()
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/')
		self.browser.find_element_by_link_text('Log out').click()

		self.login(False)
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/s')
		self.browser.find_element_by_partial_link_text('Example course').click()
		self.browser.find_element_by_link_text('Log out').click()
		
		self.login(True)
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/')
		self.browser.find_element_by_partial_link_text('Example course').click()
		self.browser.find_element_by_id('id_delete').click()
		self.browser.switch_to_alert().accept()
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/')
from .base import FunctionalTest

class ExamTest(FunctionalTest):

	def test_exam_creation_editing_and_viewing(self):
		self.browser.get("http://localhost:8000")
		self.browser.find_element_by_link_text('Log in').click()
		self.login(True)
		self.browser.find_element_by_partial_link_text('newest').click()
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/14')

		self.browser.find_element_by_link_text('Add test').click()
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/14/exams/create')

		self.browser.find_element_by_id('id_name').send_keys('Example exam')		
		self.browser.find_element_by_id('id_description').send_keys('Example description')
		self.browser.find_element_by_id('id_date_to_be_taken').send_keys('10/10/2016 10:40')
		self.browser.find_element_by_id('id_submit').click()
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/14')

		self.browser.find_element_by_partial_link_text('Example exam').click()
		self.browser.find_element_by_id('id_description').clear()
		self.browser.find_element_by_id('id_description').send_keys('Changed')
		self.browser.find_element_by_id('id_submit').click()
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/14')
		self.browser.find_element_by_link_text('Log out').click()

		self.login(False)
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/s')
		self.browser.find_element_by_partial_link_text('newest').click()
		self.browser.find_element_by_partial_link_text('Example exam').click()
		self.browser.find_element_by_link_text('Log out').click()
		
		self.login(True)
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/')
		self.browser.find_element_by_partial_link_text('newest').click()
		self.browser.find_element_by_partial_link_text('Example exam').click()
		self.browser.find_element_by_id('id_delete').click()
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/14')
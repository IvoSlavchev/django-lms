from .base import FunctionalTest

class QuestionTest(FunctionalTest):

	def test_question_creation_and_editing(self):
		self.browser.get("http://localhost:8000")
		self.browser.find_element_by_link_text('Log in').click()
		self.login(True)
		self.browser.find_element_by_partial_link_text('newest').click()
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/14')

		self.browser.find_element_by_link_text('Create new question').click()
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/14/questions/create')

		self.browser.find_element_by_id('id_name').send_keys('Example question')		
		self.browser.find_element_by_id('id_question_text').send_keys('Example question text')
		self.browser.find_element_by_id('id_form-0-choice_text').send_keys('Example choice 1')	
		self.browser.find_element_by_id('id_form-1-correct').click()
		self.browser.find_element_by_id('id_form-1-choice_text').send_keys('Example choice 2')
		self.browser.find_element_by_id('id_form-2-choice_text').send_keys('Example choice 3')
		self.browser.find_element_by_id('id_form-3-choice_text').send_keys('Example choice 4')
		self.browser.find_element_by_id('id_submit').click()
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/14')

		self.browser.find_element_by_partial_link_text('Example question').click()
		self.browser.find_element_by_id('id_question_text').clear()
		self.browser.find_element_by_id('id_question_text').send_keys('Changed')
		self.browser.find_element_by_id('id_submit').click()
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/14')

		self.browser.find_element_by_partial_link_text('Example question').click()
		self.browser.find_element_by_id('id_delete').click()
		self.browser.switch_to_alert().accept()
		self.assertEqual(self.browser.current_url, 'http://localhost:8000/courses/14')
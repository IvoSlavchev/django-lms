from .base import FunctionalTest


class QuestionTest(FunctionalTest):

	def test_question_creation_and_deletion(self):
		self.login(True)
		self.get_by_partial('newest').click()
		self.assertEqual(self.browser.current_url,
			'http://localhost:8000/courses/14')
		self.get_by_link_text('View questions').click()
		self.get_by_link_text('Create new question').click()
		self.assertEqual(self.browser.current_url,
			'http://localhost:8000/courses/14/questions/create')
		self.get_by_id('id_name').send_keys('Example question')		
		self.get_by_id('id_question_text').send_keys('Example question text')
		self.get_by_id('id_form-0-choice_text').send_keys('Example choice 1')	
		self.get_by_id('id_form-1-correct').click()
		self.get_by_id('id_form-1-choice_text').send_keys('Example choice 2')
		self.get_by_id('add-choice').click()
		self.get_by_id('id_form-2-choice_text').send_keys('Example choice 3')
		self.get_by_id('submit').click()
		self.assertEqual(self.browser.current_url,
			'http://localhost:8000/courses/14/questions/')
		self.get_by_partial('Example question').click()
		self.get_by_id('delete').click()
		self.browser.switch_to_alert().accept()
		self.assertEqual(self.browser.current_url,
			'http://localhost:8000/courses/14/questions/')
		self.logout()

	def test_question_editing(self):
		self.login(True)
		self.get_by_partial('newest').click()
		self.assertEqual(self.browser.current_url,
			'http://localhost:8000/courses/14')
		self.get_by_link_text('View questions').click()
		self.get_by_partial('Test question').click()
		self.get_by_id('id_question_text').clear()
		self.get_by_id('id_question_text').send_keys('Changed')
		self.get_by_id('submit').click()
		self.assertEqual(self.browser.current_url,
			'http://localhost:8000/courses/14/questions/')
		self.logout()
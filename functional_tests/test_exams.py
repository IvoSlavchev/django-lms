from .base import FunctionalTest


class ExamTest(FunctionalTest):

	def test_exam_creation_and_deletion(self):
		self.login(True)
		self.get_by_partial('newest').click()
		self.assertEqual(self.browser.current_url,
			'http://localhost:8000/courses/14')
		self.get_by_link_text('View exams').click()
		self.get_by_link_text('Create new exam').click()
		self.assertEqual(self.browser.current_url,
			'http://localhost:8000/courses/14/exams/create')
		self.get_by_id('id_name').send_keys('Example exam')		
		self.get_by_id('id_description').send_keys('Example description')
		self.get_by_id('id_password').send_keys('example')
		self.get_by_id('id_time_limit').send_keys('00:30')
		self.get_by_id('id_active_from').send_keys('01/01/2016 10:00')
		self.get_by_id('id_active_to').send_keys('10/10/2016 10:40')
		self.get_by_id('submit').click()
		self.assertEqual(self.browser.current_url,
			'http://localhost:8000/courses/14/exams/')
		self.get_by_partial('Example exam').click()
		self.get_by_id('delete').click()
		self.browser.switch_to_alert().accept()
		self.assertEqual(self.browser.current_url,
			'http://localhost:8000/courses/14/exams/')
		self.logout()

	def test_exam_editing(self):
		self.login(True)
		self.get_by_partial('newest').click()
		self.get_by_link_text('View exams').click()
		self.get_by_partial('newest_exam').click()
		self.get_by_id('id_description').clear()
		self.get_by_id('id_description').send_keys('Changed')
		self.get_by_id('submit').click()
		self.assertEqual(self.browser.current_url,
			'http://localhost:8000/courses/14/exams/')
		self.logout()

	def test_exam_questions_editing(self):
		self.login(True)
		self.get_by_partial('newest').click()
		self.get_by_link_text('View exams').click()
		self.get_by_partial('hurr').click()
		self.get_by_link_text('Edit questions').click()
		self.get_by_id('id_questions_1').click()
		self.get_by_id('submit').click()
		self.assertEqual(self.browser.current_url,
			'http://localhost:8000/courses/14/exams/42')
		self.logout()

	def test_exam_score_viewing(self):
		self.login(True)
		self.get_by_partial('newest').click()
		self.get_by_link_text('View exams').click()
		self.get_by_partial('hurr').click()
		self.get_by_link_text('View scores').click()
		self.assertEqual(self.browser.current_url,
			'http://localhost:8000/courses/14/exams/42/scores')
		self.logout()

	def test_exam_viewing_and_taking(self):
		self.login(False)
		self.assertEqual(self.browser.current_url,
			'http://localhost:8000/courses/s')
		self.get_by_partial('newest').click()
		self.get_by_partial('newest_exam').click()
		self.browser.get('http://localhost:8000/courses/14/exams/12/take')
		self.assertEqual(self.browser.current_url,
			'http://localhost:8000/courses/14/exams/12/s')
		self.logout()
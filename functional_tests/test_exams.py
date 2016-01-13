from .base import FunctionalTest


class ExamTest(FunctionalTest):

    def test_exam_creation_and_deletion(self):
        self.login(True)
        self.browser.get("http://localhost:8000/courses/14")
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
        self.get_by_id('id_question_count').send_keys('1')
        self.assertEqual(self.browser.current_url,
            'http://localhost:8000/courses/14/exams/create')

    def test_exam_editing(self):
        self.login(True)
        self.browser.get("http://localhost:8000/courses/14")
        self.get_by_link_text('View exams').click()
        self.get_by_partial('newest_exam').click()
        self.get_by_id('id_description').clear()
        self.get_by_id('id_description').send_keys('Changed')
        self.get_by_id('id_question_count').clear()
        self.get_by_id('id_question_count').send_keys('2')
        self.get_by_id('submit').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8000/courses/14/exams/')
        self.logout()

    def test_exam_score_viewing(self):
        self.login(True)
        self.browser.get("http://localhost:8000/courses/14")
        self.get_by_link_text('View exams').click()
        self.get_by_partial('hurr').click()
        self.get_by_link_text('View scores').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8000/courses/14/exams/42/scores')
        self.logout()

    def test_exam_viewing_taking_and_results(self):
        self.login(False)
        self.browser.get("http://localhost:8000/courses/14/s")
        self.get_by_partial('newest_exam').click()
        self.browser.get('http://localhost:8000/courses/14/exams/12/take')
        self.assertEqual(self.browser.current_url,
            'http://localhost:8000/courses/14/exams/12/s')
        self.get_by_link_text('View result').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8000/courses/14/exams/12/result')
        self.logout()
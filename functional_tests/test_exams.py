from .base import FunctionalTest


class ExamTest(FunctionalTest):

    def test_exam_creation(self):
        self.login(True)
        self.get_by_partial('Test').click()
        self.get_by_link_text('View exams').click()
        self.get_by_link_text('Create new exam').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/create')
        self.get_by_id('id_name').send_keys('Example exam')
        self.get_by_id('id_description').send_keys('Example description')
        self.get_by_id('id_password').send_keys('example')
        self.get_by_id('id_time_limit').send_keys('00:30')
        self.get_by_id('id_active_from').send_keys('2016/09/09 10:00')
        self.get_by_id('id_active_to').send_keys('2016/10/10 10:40')
        self.get_by_id('id_question_count').send_keys('1')
        self.get_by_id('submit').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/')
        header = self.browser.find_element_by_tag_name('h3').text
        self.assertEqual(header, 'Exam created successfully.')
        self.logout()

    def test_exam_deletion(self):
        self.login(True)
        self.get_by_partial('Test').click()
        self.get_by_link_text('View exams').click()
        self.get_by_partial('Test exam').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/1')
        self.get_by_id('delete').click()
        self.browser.switch_to_alert().accept()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/')
        header = self.browser.find_element_by_tag_name('h3').text
        self.assertEqual(header, 'Exam deleted successfully.')
        self.logout()

    def test_exam_editing(self):
        self.login(True)
        self.get_by_partial('Test').click()
        self.get_by_link_text('View exams').click()
        self.get_by_partial('Test exam').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/1')
        self.get_by_id('id_description').clear()
        self.get_by_id('id_description').send_keys('Changed')
        self.get_by_id('id_question_count').clear()
        self.get_by_id('id_question_count').send_keys('2')
        self.get_by_id('submit').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/')
        header = self.browser.find_element_by_tag_name('h3').text
        self.assertEqual(header, 'Exam updated successfully.')
        self.logout()

    def test_exam_score_and_questions_viewing(self):
        self.login(True)
        self.get_by_partial('Test').click()
        self.get_by_link_text('View exams').click()
        self.get_by_partial('Test exam').click()
        self.get_by_link_text('View scores').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/1/scores')
        self.get_by_link_text('Back to exam').click()
        self.get_by_link_text('View assigned questions').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/1/questions')
        self.logout()

    def test_exam_taking_and_questions_viewing(self):
        self.login(False)
        self.get_by_partial('Test').click()
        self.get_by_partial('Test exam').click()
        self.get_by_link_text('Take exam').click()
        self.browser.find_element_by_css_selector('[type="radio"]').click()
        self.get_by_id('submit').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/1/s')
        self.get_by_link_text('View exam questions').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/1/questions/s')
        self.logout()
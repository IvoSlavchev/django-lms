from .base import FunctionalTest


class ExamTest(FunctionalTest):

    def tearDown(self):
        self.logout()
        self.browser.quit()

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
        self.get_by_id('id_time_limit').click()
        self.get_by_id('submit').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/')
        message = self.get_by_class('alert').text
        self.assertEqual(message, 'Exam created successfully!')

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
        message = self.get_by_class('alert').text
        self.assertEqual(message, 'Exam deleted successfully!')

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
        message = self.get_by_class('alert').text
        self.assertEqual(message, 'Exam updated successfully!')

    def test_exam_questions_viewing(self):
        self.login(True)
        self.get_by_partial('Test').click()
        self.get_by_link_text('View exams').click()
        self.get_by_partial('Test exam').click()
        self.get_by_link_text('View assigned questions').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/1/questions')

    def test_exam_results_viewing(self):
        self.login(True)
        self.get_by_partial('Test').click()
        self.get_by_link_text('View exams').click()
        self.get_by_partial('Test exam').click()
        self.get_by_link_text('View results').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/1/results')
        self.get_by_link_text('1/1 100.0%').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/1/result/3')
        result = self.get_by_tag_name('h4').text
        self.assertEqual(result, 'Result: 1/1 100.0%')

    def test_exam_taking_and_result_viewing(self):
        self.login(False)
        self.get_by_partial('Test').click()
        self.get_by_partial('Test exam').click()
        self.get_by_link_text('Take exam').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/1/p')
        self.get_by_id('input').send_keys('example')
        self.get_by_id('submit').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/1/t')
        self.browser.find_element_by_css_selector('[type="radio"]').click()
        self.get_by_id('submit').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/1/s')
        self.get_by_link_text('View result').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/1/result/s')
        cls = self.get_by_tag_name('td').get_attribute('class')
        self.assertEqual(cls, 'success')
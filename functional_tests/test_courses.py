from .base import FunctionalTest


class CourseTest(FunctionalTest):

    def tearDown(self):
        self.logout()
        self.browser.quit()

    def test_course_creation(self):
        self.login(True)
        self.get_by_link_text('Create new course').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/create')
        self.get_by_id('id_name').send_keys('Example course')
        self.get_by_id('id_description').send_keys('Example description')
        self.get_by_id('submit').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/')
        message = self.get_by_class('alert').text
        self.assertEqual(message, 'Course created successfully!')

    def test_course_deletion(self):
        self.login(True)
        self.get_by_partial('Test').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1')
        self.get_by_id('delete').click()
        self.browser.switch_to_alert().accept()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/')
        message = self.get_by_class('alert').text
        self.assertEqual(message, 'Course deleted successfully!')

    def test_course_editing(self):
        self.login(True)
        self.get_by_partial('Test').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1')
        self.get_by_id('id_description').clear()
        self.get_by_id('id_description').send_keys('Changed')
        self.get_by_id('submit').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/')
        message = self.get_by_class('alert').text
        self.assertEqual(message, 'Course updated successfully!')

    def test_participants_editing(self):
        self.login(True)
        self.get_by_partial('Test').click()
        self.get_by_link_text('Edit participants').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/participants')
        self.get_by_id('id_participants_0').click()
        self.get_by_id('label-submit').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1')
        message = self.get_by_class('alert').text
        self.assertEqual(message, 'Participants updated successfully!')

    def test_results_viewing(self):
        self.login(True)
        self.get_by_partial('Test').click()
        self.get_by_link_text('View results').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/results')
        self.get_by_link_text('1/1 100.0%').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/exams/1/result/3')
        result = self.get_by_tag_name('h4').text
        self.assertEqual(result, 'Result: 1/1 100.0%')

    def test_course_viewing(self):
        self.login(False)
        self.get_by_partial('Test').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/s')
        course_owner = self.get_by_tag_name('td')
        self.assertEqual(course_owner.text, 'teacher')
from .base import FunctionalTest


class QuestionTest(FunctionalTest):

    def test_question_creation(self):
        self.login(True)
        self.get_by_partial('Test').click()
        self.get_by_link_text('View questions').click()
        self.get_by_link_text('Create new question').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/questions/create')
        self.get_by_id('id_name').send_keys('Example question')
        self.get_by_id('id_category').send_keys('Examples')
        self.get_by_id('id_question_text').send_keys('Example question text')
        self.get_by_id('id_form-0-choice_text').send_keys('Example choice 1')
        self.get_by_id('id_form-1-correct').click()
        self.get_by_id('id_form-1-choice_text').send_keys('Example choice 2')
        self.get_by_id('add-choice').click()
        self.get_by_id('id_form-2-choice_text').send_keys('Example choice 3')
        self.get_by_id('submit').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/questions/')
        message = self.get_by_id('messages').text
        self.assertEqual(message, 'Question created successfully.')
        self.logout()

    def test_question_deletion(self):
        self.login(True)
        self.get_by_partial('Test').click()
        self.get_by_link_text('View questions').click()
        self.get_by_partial('Test question').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/questions/1')
        self.get_by_id('delete').click()
        self.browser.switch_to_alert().accept()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/questions/')
        message = self.get_by_id('messages').text
        self.assertEqual(message, 'Question deleted successfully.')
        self.logout()

    def test_question_editing(self):
        self.login(True)
        self.get_by_partial('Test').click()
        self.get_by_link_text('View questions').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/questions/')
        self.get_by_partial('Test question').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/questions/1')
        self.get_by_id('id_category').clear()
        self.get_by_id('id_category').send_keys('Changed')
        self.get_by_id('id_question_text').clear()
        self.get_by_id('id_question_text').send_keys('Changed')
        self.get_by_id('submit').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/1/questions/')
        message = self.get_by_id('messages').text
        self.assertEqual(message, 'Question updated successfully.')
        self.logout()
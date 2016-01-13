from .base import FunctionalTest


class CourseTest(FunctionalTest):

    def test_course_creation_and_deletion(self):
        self.login(True)
        self.get_by_link_text('Create new course').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8000/courses/create')
        self.get_by_id('id_name').send_keys('Example course')
        self.get_by_id('id_description').send_keys('Example description')
        self.get_by_id('submit').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8000/courses/')
        self.get_by_partial('Example course').click()
        self.get_by_id('delete').click()
        self.browser.switch_to_alert().accept()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8000/courses/')
        self.logout()

    def test_course_editing(self):
        self.login(True)
        self.browser.get("http://localhost:8000/courses/46")
        self.get_by_id('id_description').clear()
        self.get_by_id('id_description').send_keys('Changed')
        self.get_by_id('submit').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8000/courses/')
        self.logout()

    def test_participants_editing(self):
        self.login(True)
        self.browser.get("http://localhost:8000/courses/46")
        self.get_by_link_text('Edit participants').click()
        self.get_by_id('id_participants_1').click()
        self.get_by_id('submit').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8000/courses/46')
        self.logout()

    def test_score_viewing(self):
        self.login(True)
        self.browser.get("http://localhost:8000/courses/46")
        self.get_by_link_text('View scores').click()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8000/courses/46/scores')
        self.logout()

    def test_course_viewing(self):
        self.login(False)
        self.browser.get("http://localhost:8000/courses/46/s")
        course_owner = self.browser.find_element_by_tag_name('td')
        self.assertEqual(course_owner.text, 'teacher')
        self.logout()
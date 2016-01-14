from .base import FunctionalTest


class AuthenticationTest(FunctionalTest):

    def signup(self, is_teacher):
        if is_teacher:
            self.get_by_id('id_username').send_keys('teacher_test')
            self.get_by_id('id_email').send_keys('teacher@test.net')
        else:
            self.get_by_id('id_username').send_keys('student_test')
            self.get_by_id('id_email').send_keys('student@test.net')
        self.get_by_id('id_password1').send_keys('example')
        self.get_by_id('id_password2').send_keys('example')
        self.get_by_id('submit').click()

    def test_home_page(self):
        self.browser.get("http://localhost:8081")
        header = self.browser.find_element_by_tag_name('h3').text
        self.assertEqual(header, 'Welcome!')

    def test_signup(self):
        self.browser.get("http://localhost:8081")
        self.get_by_link_text('Sign up').click()
        self.signup(True)
        self.assertEqual(self.browser.current_url, 'http://localhost:8081/')
        self.get_by_link_text('Sign up').click()
        self.signup(False)

    def test_login_and_logout(self):
        self.login(True)
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/')
        self.logout()
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/login')
        self.login(False)
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/s')
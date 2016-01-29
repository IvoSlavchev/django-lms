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

    def test_home(self):
        header = self.get_by_tag_name('h3').text
        self.assertEqual(header, 'Welcome!')

    def test_signup(self):
        self.get_by_id('signup').click()
        self.assertEqual(self.browser.current_url, 'http://localhost:8081/signup')
        self.signup(True)
        self.assertEqual(self.browser.current_url, 'http://localhost:8081/')
        message = self.get_by_class('alert').text
        self.assertEqual(message, 'Check email for a confirmation link!')
        self.get_by_id('signup').click()
        self.signup(False)
        self.assertEqual(self.browser.current_url, 'http://localhost:8081/')

    def test_login_and_logout(self):
        self.login(True)
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/')
        self.logout()
        message = self.get_by_class('alert').text
        self.assertEqual(message, 'Logged out!')
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/')
        self.login(False)
        self.assertEqual(self.browser.current_url,
            'http://localhost:8081/courses/s')
        self.logout()

    def test_valid_confirmation(self):
        self.browser.get('http://localhost:8081/confirm?q=valid')
        message = self.get_by_class('alert').text
        self.assertEqual(message, 'Successfully confirmed!')

    def test_exipred_confirmation_key(self):
        self.browser.get('http://localhost:8081/confirm?q=expired')
        message = self.get_by_class('alert').text
        self.assertEqual(message, 'Link expired!')
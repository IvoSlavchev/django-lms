from .base import FunctionalTest


class StyleTest(FunctionalTest):

    def test_correct_bootstrap_class(self):
        self.browser.get('http://localhost:8081')
        cls = (self.get_by_link_text('Django-LMS')
            .get_attribute('class'))
        self.assertEqual(cls, 'navbar-brand')

        cls = (self.get_by_link_text('Log in')
            .get_attribute('class'))
        self.assertEqual(cls, 'btn navbar-btn navbar-right')

        cls = (self.browser.find_element_by_tag_name('h3')
            .get_attribute('class'))
        self.assertEqual(cls, 'text-primary text-center')
from .base import FunctionalTest


class StyleTest(FunctionalTest):

    def test_correct_bootstrap_class(self):
        self.browser.get('http://localhost:8081')
        cls = self.get_by_link_text('Django-LMS').get_attribute('class')
        self.assertEqual(cls, 'navbar-brand')
        cls = self.get_by_tag_name('button').get_attribute('class')
        self.assertEqual(cls, 'btn btn-primary')
        cls = self.get_by_tag_name('h3').get_attribute('class')
        self.assertEqual(cls, 'text-primary text-center')
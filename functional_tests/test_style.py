from .base import FunctionalTest


class StyleTest(FunctionalTest):

	def test_correct_bootstrap_class(self):
		self.browser.get("http://localhost:8081")
		elem_class = (self.get_by_link_text('Django-LMS')
			.get_attribute("class"))
		self.assertEqual(elem_class, 'navbar-brand')

		elem_class = (self.get_by_link_text('Log in')
			.get_attribute("class"))
		self.assertEqual(elem_class, 'btn navbar-btn navbar-right')

		elem_class = (self.browser.find_element_by_tag_name('h3')
			.get_attribute("class"))
		self.assertEqual(elem_class, 'text-primary text-center')
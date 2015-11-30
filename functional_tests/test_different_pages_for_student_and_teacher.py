from .base import FunctionalTest

class DifferentPagesTest(FunctionalTest):

	def test_if_something_even_works(self):
		self.browser.get("http://localhost:8000")
		header = self.browser.find_element_by_tag_name('h1').text
		self.assertEqual(header, 'Welcome to the Django-LMS!')

	def test_teacher_page(self):
		self.browser.get("http://localhost:8000")
		self.browser.find_element_by_link_text('Login as Teacher').click()
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertIn('Teacher', page_text)

	def test_student_page(self):
		self.browser.get("http://localhost:8000")
		self.browser.find_element_by_link_text('Login as Student').click()
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertIn('Student', page_text)
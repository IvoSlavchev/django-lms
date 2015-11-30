from .base import FunctionalTest

class DifferentPagesTest(FunctionalTest):

	def test_teacher_page(self):
		self.browser.find_element_by_link_text('Login as teacher').click()
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertIn('Teacher', page_text)

	def test_student_page(self):
		self.browser.find_element_by_link_text('Login as student').click()
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertIn('Student', page_text)
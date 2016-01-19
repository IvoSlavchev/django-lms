from .base import FunctionalTest

import time

class AdminTest(FunctionalTest):

	def login_admin(self):
		self.browser.get("http://localhost:8081/admin")
		self.get_by_id('id_username').send_keys('admin')
		self.get_by_id('id_password').send_keys('admin')
		self.browser.find_element_by_xpath('//input[@type="submit"]').click()

	def test_login(self):
		self.login_admin()
		self.assertEqual(self.browser.current_url,
			"http://localhost:8081/admin/")

	def test_objects_view(self):
		self.login_admin()
		self.get_by_link_text('Courses').click()
		self.get_by_link_text('Test').click()
		self.assertEqual(self.browser.current_url,
			"http://localhost:8081/admin/courses/course/1/change/")
		self.get_by_link_text('Home').click()
		self.assertEqual(self.browser.current_url,
			"http://localhost:8081/admin/")
		
	def test_objects_edit(self):
		self.login_admin()
		self.get_by_link_text('Users').click()
		self.get_by_link_text('teacher').click()
		self.assertEqual(self.browser.current_url,
			"http://localhost:8081/admin/users/user/1/change/")
		self.get_by_id('id_username').clear()
		self.get_by_id('id_username').send_keys('changed')
		self.browser.find_element_by_xpath('//input[@type="submit"]').click()
		self.assertEqual(self.browser.current_url,
			"http://localhost:8081/admin/users/user/")
		text = self.browser.find_element_by_tag_name('li').text
		self.assertEqual(text, 'The user "changed" was changed successfully.')

	def test_objects_delete(self):
		self.login_admin()
		self.get_by_link_text('Users').click()
		self.get_by_link_text('teacher').click()
		self.assertEqual(self.browser.current_url,
			"http://localhost:8081/admin/users/user/1/change/")
		self.get_by_link_text('Delete').click()
		self.assertEqual(self.browser.current_url,
			"http://localhost:8081/admin/users/user/1/delete/")
		self.browser.find_element_by_xpath('//input[@type="submit"]').click()
		self.assertEqual(self.browser.current_url,
			"http://localhost:8081/admin/users/user/")
		text = self.browser.find_element_by_tag_name('li').text
		self.assertEqual(text, 'The user "teacher" was deleted successfully.')
import re

from omnirose.live_tests import OmniRoseSeleniumTestCase, LoginFailedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from django.core import mail

class AccountLiveTests(OmniRoseSeleniumTestCase):

    fixtures = ['test_user_data']

    def test_account_creation(self):
        sel = self.selenium

        self.get_home()
        sel.find_element_by_link_text('create account').click()

        # Enter the email address
        email = 'joe@test.com'
        create = ActionChains(sel)
        create.send_keys(email)
        create.send_keys(Keys.RETURN)
        create.perform()

        # Check that we're now logged in
        self.assertLoggedInAs(email)

        # Check that we were send an email with a password in
        self.assertEqual(len(mail.outbox), 1)
        password = re.search(r'password: (\S+)', mail.outbox[0].body).group(1)
        self.assertTrue(password)

        # Log out and check that we can log in with the new password
        self.logout()
        self.login(email, password)

    def test_good_logins(self):
        self.login('bob@test.com', 'secret')

    def test_bad_logins(self):
        # Test valid login (for sanity)
        with self.assertRaises(LoginFailedException):
            self.login('bob@test.com', 'wrongpassword')

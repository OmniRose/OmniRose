import re

from time import sleep

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

    def test_forgotten_password(self):
        sel = self.selenium

        # go to forgotten password page
        self.get_home()
        sel.find_element_by_link_text('log in').click()
        sel.find_element_by_link_text('Forgotten your password?').click()

        # enter email address
        email = 'bob@test.com'
        create = ActionChains(sel)
        create.send_keys(email)
        create.send_keys(Keys.RETURN)
        create.perform()
        sleep(0.5)

        # get the reset url from the email
        self.assertEqual(len(mail.outbox), 1)
        reset_link = re.search(r'(\S+accounts/reset\S+)', mail.outbox[0].body).group(1)
        self.assertTrue(reset_link)

        # go to reset page
        new_password = 'new_password'
        sel.get(reset_link)
        reset = ActionChains(sel)
        reset.send_keys(new_password)
        reset.send_keys(Keys.TAB)
        reset.send_keys(new_password)
        reset.send_keys(Keys.RETURN)
        reset.perform()

        # Try logging in with the new password
        sel.find_element_by_link_text('Log in').click()
        self.login('bob@test.com', new_password)

        # check that old password does not work now
        self.logout()
        with self.assertRaises(LoginFailedException):
            self.login('bob@test.com', 'secret')

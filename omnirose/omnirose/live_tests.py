from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings

class LoginFailedException(Exception):
    pass

class OmniRoseSeleniumTestCase(StaticLiveServerTestCase):

    # def __init__(self, *args, **kwargs):
    #     super(OmniRoseSeleniumTestCase, self).__init__(*args, **kwargs)
    #     if settings.DEBUG == False:
    #         settings.DEBUG = True

    @classmethod
    def setUpClass(cls):
        super(OmniRoseSeleniumTestCase, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(OmniRoseSeleniumTestCase, cls).tearDownClass()

    def get_home(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))

    def logout(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/logout'))

    def login(self, email='bob@test.com', password='secret'):
        sel = self.selenium

        self.get_home()
        sel.find_element_by_link_text('log in').click()

        login = ActionChains(sel)
        login.send_keys(email)
        login.send_keys(Keys.TAB)
        login.send_keys(password)
        login.send_keys(Keys.RETURN)
        login.perform()

        self.assertLoggedInAs(email)

    def assertLoggedInAs(self, email):
        sel = self.selenium

        try:
            user_menu = sel.find_element_by_link_text(email)
            self.assertTrue(user_menu)
            user_menu.click()
            logout_link = sel.find_element_by_link_text('logout')
            self.assertTrue(logout_link)
            user_menu.click() # to close it again
        except NoSuchElementException:
            raise LoginFailedException()

import os
from selenium.webdriver import Chrome, ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, StaleElementReferenceException
import path

__version__ = "1.0.0"


class Rakuten(object):
    """楽天銀行"""

    _login_page = 'http://www.rakuten-bank.co.jp/business/plus/'

    _wait = 10

    def __init__(self, browser='chrome'):
        if browser == 'chrome':
            self.browser = Chrome(os.path.join(path.DRIVERS, 'chromedriver'))
        else:
            raise Exception(f"Driver {browser} dose not exist!")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.quit()

    def login(self, login_id, login_pwd):
        """
        ログイン
        :param str login_id: ログインID
        :param str login_pwd: ログインパスワード
        :return:
        """
        # ログインページに移動
        self.browser.get(self._login_page)

        # ログインする
        self.browser.find_element_by_xpath("//a[@href='https://fes.rakuten-bank.co.jp/MS/main/RbS?COMMAND=START&CurrentPageID=SWITCH_PAGE']").click()
        for handle in self.browser.window_handles:
            print(handle)



if __name__ == '__main__':
    import time
    with Rakuten() as rakuten:
        rakuten.login('acc', 'pwd')
        time.sleep(10)

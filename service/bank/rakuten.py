import os
from datetime import date, timedelta
from selenium.webdriver import Chrome, ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, StaleElementReferenceException
import path
from service.bank import BaseBank
from util.extension import retry
from util.exceptions import IncorrectDataException

__version__ = "2.0.0"


class Rakuten(BaseBank):
    """楽天銀行"""

    __login_page = 'http://www.rakuten-bank.co.jp/business/plus/'
    __top_page = ''

    __wait = 10

    def __init__(self, login_id=None, login_pwd=None, browser='chrome'):
        self.__login_id = login_id
        self.__login_pwd = login_pwd

        if browser == 'chrome':
            self.__browser = Chrome(os.path.join(path.DRIVERS, 'chromedriver'))
        else:
            raise Exception(f"Driver {browser} dose not exist!")

        if login_id is not None and login_pwd is not None:
            self.login(login_id, login_pwd)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
        self.__browser.quit()

    @retry(times=1)
    def login(self, login_id=None, login_pwd=None):
        """
        ログイン
        :param str login_id: ログインID
        :param str login_pwd: ログインパスワード
        :return: None
        """
        login_id = self.__login_id if login_id is None else login_id
        login_pwd = self.__login_pwd if login_pwd is None else login_pwd

        # ログインページに移動
        self.__browser.get(self.__login_page)

        # ログインする
        self.__browser.find_element_by_xpath("//a[@href='https://fes.rakuten-bank.co.jp/MS/main/RbS?COMMAND=START&CurrentPageID=SWITCH_PAGE']").click()
        self.__browser.switch_to.window(self.__browser.window_handles[1])

        self.__browser.find_element_by_id('LOGIN:USER_ID').send_keys(login_id)
        self.__browser.find_element_by_id('LOGIN:LOGIN_PASSWORD').send_keys(login_pwd)
        self.__browser.find_element_by_id('LOGIN:_idJsp85').click()

        if True:  # TODO ログイン成功
            self.__login_id = login_id
            self.__login_pwd = login_pwd

    def logout(self):
        """
        ログアウト
        :return: None
        """
        pass

    def transfer(self, transaction, security_pwd, otp_getter=lambda: str()):
        """
        自動出金
        :param dict transaction: 取引情報
        :param str security_pwd: 取引暗証
        :param callback otp_getter: ワンタイムパスワードの取得方法
        :return:
        """
        # トップページに移動 TODO リンクがあるかどうかを判断し、ページ移動の実行
        self.__browser.get(self.__top_page)

        self.__browser.find_element_by_xpath("//a[contains(@href, '/MS/main/gns?COMMAND=TRANSFER_MENU_START&&CurrentPageID=HEADER_FOOTER_LINK')]").click()
        self.__browser.find_element_by_link_text('振込を行う').click()

        if transaction[0] == '0036':
            # 楽天対楽天
            self.__browser.find_element_by_id('jspBankSearchExtra:SELECT_BANK:_idJsp132').click()

            Select(self.__browser.find_element_by_name('FORM:SELECT_CREDIT_BRANCH')).select_by_value(transaction[1])

            # 口座番号の入力
            self.__browser.find_element_by_id('FORM:CREDIT_ACCOUNT_NUMBER').send_keys(transaction[3])

            # 金額の入力
            self.__browser.find_element_by_id('FORM:AMOUNT').send_keys(transaction[4])

            # 確認ボタン
            self.__browser.find_element_by_id('FORM:_idJsp257').click()

        else:
            # 楽天対他行
            self.__browser.find_element_by_id('jspBankSearchExtra:EXTRA_BANK_OPEN:_idJsp222').click()

            # 銀行番号の入力
            self.__browser.find_element_by_id('jspBankSearchExtra:CODE_SEARCH:BANK_CODE').send_keys(transaction[0])

            self.__browser.find_element_by_id('jspBankSearchExtra:CODE_SEARCH:_idJsp283').click()

            # 支店番号を入力
            self.__browser.find_element_by_id('jspBranchSearch:CODE_SEARCH:BRANCH_CODE').send_keys(transaction[1])
            self.__browser.find_element_by_id('jspBranchSearch:CODE_SEARCH:_idJsp149').click()

            # TODO if browser.find_by_text(unicode('ご指定の銀行情報は存在しません', 'utf8')):

            # TODO CODE DRY
            if transaction[2] == "0":
                Select(self.__browser.find_element_by_name('FORM:_idJsp137')).select_by_value('1')
            elif transaction[2] == "1":
                Select(self.__browser.find_element_by_name('FORM:_idJsp137')).select_by_value('2')
            else:
                # TODO Error Message
                raise IncorrectDataException('楽天銀行出金：対応できない振込先口座科目があります・')

            # 口座番号の入力
            self.__browser.find_element_by_id('FORM:CREDIT_ACCOUNT_NUMBER').send_keys(transaction[3])

            # 金額の入力
            self.__browser.find_element_by_id('FORM:AMOUNT').send_keys(transaction[4])

            # 確認ボタン
            self.__browser.find_element_by_id('SECURITY_BOARD:_idJsp829').click()

        error = next(iter(self.__browser.find_elements_by_class_name('errortxt')), None)
        if error:
            # 間違い振込情報
            raise IncorrectDataException(error.text)
        else:
            # ワンタイムパスワード送信
            self.__browser.find_element_by_id('SECURITY_BOARD:_idJsp496').click()

        # ワンタイムパスワードの入力
        one_time_pwd = otp_getter()
        self.__browser.find_element_by_id('SECURITY_BOARD:SECURITY_CODE').send_keys(one_time_pwd)

        # 取引暗証の入力
        self.__browser.find_element_by_id('SECURITY_BOARD:USER_PASSWORD').send_keys(security_pwd)

        # 出金確認
        # TODO find_element_by_text('button....')
        if self.__browser.find_elements_by_id('SECURITY_BOARD:_idJsp891'):
            self.__browser.find_element_by_id('SECURITY_BOARD:_idJsp891').click()
        elif self.__browser.find_elements_by_id('SECURITY_BOARD:_idJsp949'):
            self.__browser.find_element_by_id('SECURITY_BOARD:_idJsp949').click()
        elif self.__browser.find_elements_by_id('SECURITY_BOARD:_idJsp963'):
            self.__browser.find_element_by_id('SECURITY_BOARD:_idJsp963').click()
        elif self.__browser.find_elements_by_id('SECURITY_BOARD:_idJsp905'):
            # rakuten to rakuten
            self.__browser.find_element_by_id('SECURITY_BOARD:_idJsp905').click()
        else:
            # 時間外振込予約実行
            self.__browser.find_element_by_id('SECURITY_BOARD:_idJsp961').click()

        # TODO 結果判断
        # if browser.is_text_present(unicode('お取引を続けることができません。', 'utf-8')):
        #     browser.quit()
        #     raise Exception('楽天銀行出金：WEB ERROR:ワンタイムパスワードが間違いました。')
        # if browser.is_text_present(unicode('以下の振込依頼を受付ました。', 'utf-8')):
        #     return browser

    def history(self, start_date=None, end_date=date.today()):
        """
        履歴を取る
        :param date start_date: 開始日時
        :param date end_date: 開始日時
        :return: None
        """
        if start_date is None:
            start_date = end_date

        # トップページに移動 TODO リンクがあるかどうかを判断し、ページ移動の実行
        self.__browser.get(self.__top_page)

        self.__browser.find_element_by_xpath("//a[contains(@href, '/MS/main/gns?COMMAND=CREDIT_DEBIT_INQUIRY_START&&CurrentPageID=HEADER_FOOTER_LINK')]").click()

        # 日時範囲を入力する
        self.__browser.find_element_by_id('FORM_DOWNLOAD_AP_2:EXPECTED_DATE_FROM_YEAR').send_keys(start_date.strftime('%Y'))
        self.__browser.find_element_by_id('FORM_DOWNLOAD_AP_2:EXPECTED_DATE_FROM_MONTH').send_keys(start_date.strftime('%m'))
        self.__browser.find_element_by_id('FORM_DOWNLOAD_AP_2:EXPECTED_DATE_FROM_DAY').send_keys(start_date.strftime('%d'))
        self.__browser.find_element_by_id('FORM_DOWNLOAD_AP_2:EXPECTED_DATE_TO_YEAR').send_keys(end_date.strftime('%Y'))
        self.__browser.find_element_by_id('FORM_DOWNLOAD_AP_2:EXPECTED_DATE_TO_MONTH').send_keys(end_date.strftime('%m'))
        self.__browser.find_element_by_id('FORM_DOWNLOAD_AP_2:EXPECTED_DATE_TO_DAY').send_keys(end_date.strftime('%d'))

        # TODO Pagination?
        # CSVをダウンロードする
        self.__browser.find_element_by_id('FORM_DOWNLOAD_AP_2:_idJsp313').click()

        # Alert accept
        self.__browser.switch_to.alert.accept()

        # TODO if browser.is_text_present('指定された期間にはお取引はございません。')
        #     raise IncorrectDataException('.......')

    def run_test(self):
        self.__browser.get('http://www.baidu.com')

        a = self.__browser.find_element_by_class_name('baiddddd')

        a.click()


if __name__ == '__main__':
    import time
    with Rakuten(1) as rakuten:
        rakuten.login('acc', 'pwd')
        time.sleep(10)
        # rakuten.history()

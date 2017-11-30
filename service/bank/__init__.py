import os
import requests
from selenium.webdriver import Chrome
import path


class BaseBank(object):
    @staticmethod
    def get_one_time_pwd(through='thunderbird', **kwargs):
        """
        ワンタイムパスワードの取得
        :param str through: 取得方法
        :param dict kwargs: 必要情報
        :return:
        """
        if through == 'thunderbird':
            pass
        elif through == 'smtp':
            pass
        else:
            # API経由で取得
            response = requests.post(url=through, json={'token': kwargs['token']})


from .rakuten import Rakuten

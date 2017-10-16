class Elements(object):
    """ページ要素"""

    def __init__(self, elements):
        """
        サイトのページ要素
        :param list elements:Element
        """
        for element in elements:
            self.__setattr__(element.key, element.value)


if __name__ == '__main__':
    class Ele(object):
        def __init__(self, key, value):
            self.key = key
            self.value = value

    e1 = Ele('title', '标题')
    e2 = Ele('name', '名字')
    e3 = Ele('author', '作者')
    e4 = Ele('content', '内容')

    es = [e1, e2, e3, e4]

    bigE = Elements(es)

    print(vars(bigE))

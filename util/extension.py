from selenium.common.exceptions import NoSuchElementException


def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except NoSuchElementException as e:
            print(e.msg)
            raise
        except:
            raise
    return wrapper


def retry(times):
    def _retry(func):
        def wrapper(*args, **kwargs):
            for i in range(0, times):
                try:
                    func(*args, **kwargs)
                except:
                    if i == times - 1:
                        raise
                else:
                    break
        return wrapper
    return _retry


if __name__ == '__main__':
    import random

    class Ts(object):
        change = 0

        def ef(self):
            return self.change == 1

        @retry(3)
        def pr(self):
            ri = random.randint(100, 101)
            print(ri)
            if ri == 100:
                print('ppppp')
            else:
                raise Exception('a ex')


    t = Ts()
    t.pr()

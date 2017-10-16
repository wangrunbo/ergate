import os


ROOT = os.path.dirname(os.path.abspath(__file__))

DRIVERS = os.path.join(ROOT, 'drivers')


if __name__ == '__main__':
    print(ROOT, DRIVERS)

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from controllers.tribute_controller import get_tribute_data

def check():
    # User ID 3 is Kanna
    res = get_tribute_data(3)
    print("User Stats:")
    print(res['data']['user_stats'])

if __name__ == '__main__':
    check()

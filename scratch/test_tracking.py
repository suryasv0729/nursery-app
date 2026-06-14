import sys
import os
import time
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from controllers.order_controller import get_order_tracking

def test():
    for _ in range(5):
        res = get_order_tracking(5, 3) # Order 5, User 3
        data = res['data']
        print(f"Progress: {data['progress']}, Lat: {data['current_lat']}, Lng: {data['current_lng']}")
        time.sleep(1)

if __name__ == '__main__':
    test()

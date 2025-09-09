# -*- coding: utf-8 -*-

def price_round(price):
    '''2舍3入，个位保留0和5'''
    price = int(price)
    if 0 <= price % 5 <= 2:
        return int(5 * (price // 5))
    else:
        return int(5 * (price // 5) + 5)
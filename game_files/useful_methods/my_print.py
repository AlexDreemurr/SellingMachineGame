import time

def my_print(text, time_delay, ender = "\n"):
    '''模拟逐字打印文本，time_delay为打印每个字符的间隔时间
                        ender为句末打印（默认为换行）'''
    for char in text:
        print(char, end = "", flush = True)
        time.sleep(time_delay)
    print(ender, end = "")

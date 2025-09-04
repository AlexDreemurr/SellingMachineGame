# -*- coding: utf-8 -*-

numbers = list("1234567890")

def space_counter(text: str, limit_length: int, mode = "right"):
    '''给定字符串和指定长度，返回右侧填补空格至指定长度的字符串
       right: 右侧留白
       middle: 居中'''
    
    text_length = my_len(text)

    if (limit_length - text_length) <= 0:
        return text
    
    if mode == "middle":
        left_blank = (limit_length - text_length) // 2
        right_blank = limit_length - text_length - left_blank

        return " " * left_blank + text + " " * right_blank
    
    return text + " " * (limit_length - text_length)
    
def my_len(text: str):
    '''返回字符串的计算长度'''
    text_length = 0
    numbers = list("0123456789")
    

    # \x1b 为颜色字转义字符，1长度
    if text[0] == '\x1b':
        index = text.find("m")
        for char in text[index + 1:]:
            # 汉字范围
            if 13312 <= ord(char) <= 40959:
                text_length += 2
            elif char in numbers:
                text_length += 1
            elif char == "%":
                text_length += 1
            # 遇到了结尾\033，直接滚蛋
            if char == "\033":
                break

    else:
        for char in text:
            if 13312 <= ord(char) <= 40959:
                text_length += 2
            elif char == "〇":
                text_length += 2
            else:
                text_length += 1
    
    return text_length

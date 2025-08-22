# -*- coding: utf-8 -*-

def space_counter(text: str, limit_length: int, mode = "right", length = 0):
    '''给定字符串和指定长度，返回右侧填补空格至指定长度的字符串
       right: 右侧留白
       middle: 居中'''
    if length != 0:
        text_length = length
    else:
        text_length = 0

        if text[0] == '\x1b':
            for char in text:
                if 13312 <= ord(char) <= 40959:
                    text_length += 2
        else:
            for char in text:
                if 13312 <= ord(char) <= 40959:
                    text_length += 2
                else:
                    text_length += 1

    if (limit_length - text_length) <= 0:
        return text
    
    if mode == "middle":
        left_blank = (limit_length - text_length) // 2
        right_blank = limit_length - text_length - left_blank

        return " " * left_blank + text + " " * right_blank
    
    return text + " " * (limit_length - text_length)
    

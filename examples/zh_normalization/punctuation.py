"""
去除字符串中的标点符号
"""
import re
import time
from string import punctuation
from functools import wraps

# 英文标点符号
punctuation_en = r"!"#$%&'（）《》()*+,-./:;<=>?@[\]^_`{|}~"
# 中文标点符号
punctuation_zh = r"'＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。'"
# 混合
remove_chars = '[·!"\#$%&\'()＃！（）*+,-./:;<=>?\@，：?￥★、…．＞【】［］《》？“”‘’\[\\]^_`{|}~]+'


def timer(function):
    '''
    用装饰器实现函数计时
    :param function: 需要计时的函数
    :return: None
    '''
    @wraps(function)
    def function_timer(*args, **kwargs):
        fun_name = function.__name__
        print('%s start...]'%fun_name)
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print('%s finished, spent time: %.3f s]'%(fun_name, t1 - t0))
    
        return result
        
    return function_timer


@timer
def replace_punctuation_tran(strs:str):
    """去除字符串中的标点符号
    使用 str.translate() 函数
    """
    str_new = strs.replace(' ', '')
    str_new = str_new.translate(str.maketrans('', '', remove_chars))
    
    return str_new


@timer
def replace_punctuation_re(strs:str):
    """去除字符串中的标点符号
    使用正则表达式从字符串中查找和删除标点符号
    """
    
    str_new = strs.replace(' ', '')
    str_new = re.sub(remove_chars, '', str_new)

    return str_new


def test():
    text = '+今天=是！2021!   年/8月?1,7日★.---《七夕节@》：让我*们出门（#@）去“感受”夏天的荷尔蒙！'
    print(replace_punctuation_tran(text))
    print(replace_punctuation_re(text))


if __name__ == "__main__":
    test()
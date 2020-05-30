"""
数据保存到txt文件
lichuan
lc@dlc618.com
"""

def write_txt_single_str(write_list, write_name):
    """
    每行一个数据保存到txt
    input：
        write_list    要保存的列表
        write_path    要保存的txt路径
    return：
        result        保存状态
    """
    for value in write_list:
        with open (write_name, 'a') as f:
            text = str(value) + '\n'
            f.write(text)

    return 'Success'


if __name__ == "__main__":
    single_str = [0,1,2,3,3,4,5]
    write_name = '/media/lc/Data/modle_and_code/Python/learn_note/note_basic/test.txt'

    a = write_txt_single_str(single_str, write_name)

    print(a)

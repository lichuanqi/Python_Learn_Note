'''
@Description: 读取txt文件笔记 待补充
@Autor: lichuan
'''


def read_txt_single_str(txt_path):
    """
    @Doc:txt文件中一行一个数值
    @txt：文件路径
    @return：数值列表
    """
    data = []

    with open (txt_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # 抓换成数值
            line_int = int(line.strip('\n'))
            data.append(line_int)

    return data


def read_txt_multiple_str(txt_path):
    """
    @Doc:txt文件中一行多个数值读取
    @txt：文件路径
    @return：多个列表
    """
    part_01 = []
    part_02 = []
    part_03 = []

    with open (txt_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # 抓换成数值
            line_str = line.strip('\n')
            line_str_ = line_str.split(',')
 
            part_01.append(int(line_str_[0]))
            part_02.append(int(line_str_[1]))
            part_03.append(int(line_str_[2]))

    return part_01, part_02, part_03


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

    our_part = '/media/lc/Data/modle_and_code/data/number/our_part_03.txt'
    part_01, part_02, part_03 = read_txt_multiple_str(our_part)

    print(part_01)


    single_str = [0,1,2,3,3,4,5]
    write_name = '/media/lc/Data/modle_and_code/Python/learn_note/note_basic/test.txt'

    a = write_txt_single_str(single_str, write_name)

    print(a)


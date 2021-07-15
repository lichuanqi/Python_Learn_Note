"""
@计算两个矩形框的交幷比
@lichuan
@lc@dlc618.com
"""

def get_IoU(box1, box2):
    """
    @description：计算两个矩形框的交幷比
    @box1：矩形框左上角坐标 宽度 高度，（x1, y1, w1, h1）
    @box2：矩形框左上角坐标 宽度 高度，（x2, y2, w2, h2）
    @return:交幷比
    """
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    # 分别计算两个矩形框的面积
    area_box1 = w1 * h1
    area_box2 = w2 * h2

    # 计算相交矩形的宽度和高度和面积
    d_w = max(0, (min(x1+w1, x2+w2) - max(x1, x2)))
    d_h = max(0, (min(y1+h1, y2+h2) - max(y1, y2)))  
    area_intersect = d_w * d_h

    # 交幷比
    IoU = area_intersect / (area_box1 + area_box2 - area_intersect)

    return IoU


if __name__ == '__main__':
    box_1 = (0, 0, 10, 10)
    box_2 = (5, 5, 10, 10)
    IoU = get_IoU(box_1, box_2)
    print("IoU是：{}".format(IoU))
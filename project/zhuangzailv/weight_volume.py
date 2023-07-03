"""研究邮件重量与体积的相关性"""
import sys
import math
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd 
from matplotlib import colors
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from sklearn.neighbors import LocalOutlierFactor
import pymysql


class DBMySQL():
    def __init__(self) -> None:
        # 连接数据库
        mysql_host =  host='192.168.35.221'
        mysql_user='root'
        mysql_password='123456'
        mysql_database='test'
        self.conn = pymysql.connect(host=mysql_host,
                            user=mysql_user, 
                            passwd=mysql_password,
                            database=mysql_database)  
        # 创建游标对象  
        self.cursor = self.conn.cursor()

    def select_all_data(self):
        # 查看表数据
        sql =  "SELECT * FROM `zzl_dws_data`"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print(result)

    def select_weight_volume(self, _org=None, _loc=None, _rout=None, _date=None):
        """筛选重量和体积数据

        Params
            _org, _loc, _rout, _date
        Return
            x,y
        """
        sql = """SELECT calculate_weight,calculate_volume FROM `zzl_dws_data`"""

        if not all([_org, _loc, _rout, _date]):
            return '不限制筛选条件'
        
        sql += """ WHERE"""
        if _org is not None:
            sql += """ org_name='%s'"""%_org
        if _loc is not None:
            sql += """ and dws_location='%s'"""%_loc
        if _rout is not None:
            sql += """ and email_router='%s'"""%_rout
        if _date is not None:
            sql += """ and calculate_label='%s'"""%_date

        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
    
    def select_result(self, org, loc, rout, date):
        """查询相关计算数据
        
        Params
            org, loc, rout, date
        Return
            weight_range_left,average_volume,volume_range_frequency,volume_range_probability
        """
        sql = """SELECT weight_range_left,average_volume,volume_range_frequency,volume_range_probability
                 FROM `zzl_dws_result`"""
        
        if not all([ org, loc, rout, date]):
            return '不限制筛选条件'

        sql += """ WHERE"""
        if org is not None:
            sql += """ org_name='%s'"""%org
        if loc is not None:
            sql += """ and dws_location='%s'"""%loc
        if rout is not None:
            sql += """ and email_router='%s'"""%rout
        if date is not None:
            sql += """ and calculate_label='%s'"""%date
        
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result


    def insert_result(self, data):
        """计算数据插入到计算数据表
        Params
            data: (org, loc, rout, date, x_left, average_volume, frequency, probability)
        Return
            status
        """
        sql = """INSERT INTO zzl_dws_result (
                    org_name,dws_location,email_router,calculate_label, 
                    weight_range_left,average_volume,volume_range_frequency,volume_range_probability)
                 VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s)"""
        # 插入数据
        self.cursor.executemany(sql, data)
        # 提交事务并关闭连接  
        self.conn.commit()

    def txt2mysql(self, txtfile):
        """把txt数据插入到MySQL中"""
        x, y = read_data_txt(txtfile)
        i = 0
        for _x,_y in zip(x,y):
            # if i >=10:
            #     continue

            print('开始处理第%s条数据'%i)
            time_now = datetime.now()
            collection_time = time_now.timestamp()
            calculate_label = time_now.strftime("%Y%m")  
            calculate_weight = int(_x)
            calculate_volume = int(_y)

            sql = """INSERT INTO zzl_dws_data (
                        org_name, dws_id, dws_location,
                        email_id, email_router, basic_product_name,article_property,
                        measurement_weight,measurement_length,measurement_width,measurement_height,
                        collection_time,calculate_label,calculate_weight,calculate_volume)
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            data = ('合肥蜀山(23000071)', 'dws001', '双层+小件机',
                    'e1111111', '合肥-芜湖', '标快', '物品',
                    _x, 0, 0, 0,
                    time_now, calculate_label,calculate_weight,calculate_volume)
            print(data)
            # 插入数据  
            self.cursor.execute(sql, data)  

            # 提交事务并关闭连接  
            self.conn.commit()

            i += 1

    def __del__(self) -> None:
        # 关闭数据库连接
        self.conn.close()


def read_data_txt(txtfile):
    """从txt文档中读取重量体积数据
    
    Params
        txtfile: txt文件路径,数据保存格式如下
            1.3400,14.4370 
            4.1700,39.9230 
            1.6100,13.5050 
            2.4900,23.6430 
            ...

    Return
        x 所有的重量数据
        y 所有体积数据
    """
    x, y = [], []
    with open(txtfile) as f:
        for line in f.readlines():
            _x, _y = line.strip().split(',')
            x.append(float(_x))
            y.append(float(_y))
    
    return x,y


def txt_to_mysql():
    dbmysql = DBMySQL()
    txtfile = 'project/zhuangzailv/data_dws_hefei.txt'
    dbmysql.txt2mysql(txtfile)


def calculate_matrix_own(x,y):
    """通过手搓计算x和y的相关性矩阵"""
    # 数据区间
    xx = np.arange(0,11,1)
    # print(type(xx), xx)
    xx_headers = []
    for i in range(len(xx)):
        if i < len(xx)-1:
            xx_headers.append('%s-%s'%(xx[i], xx[i+1]))
        else:
            xx_headers.append('%s+'%(xx[i]))       
    print(xx_headers)

    yy = np.arange(0,101,4)
    # print(type(yy), yy)
    yy_headers = []
    for i in range(len(yy)):
        if i < len(yy)-1:
            yy_headers.append('%s-%s'%(yy[i], yy[i+1]))
        else:
            yy_headers.append('%s+'%(yy[i]))
    print(yy_headers)

    nums = np.zeros((len(xx),len(yy)))
    print(nums.shape)

    for _x,_y in zip(x,y):
        print('原始数据: %s,%s'%(_x,_y))
        
        # 确定行索引
        if _x > xx[-1]:
            _i = len(xx) - 1
        else:
            _i = math.floor(_x)
        
        # 确定列索引
        if _y > yy[-1]:
            _j = len(yy) - 1
        else:
            _j = int(_y) // 4

        print('计数矩阵索引号: %s,%s'%(_i, _j))
        nums[_i, _j] += 1


    return nums


def calculate_matrix_np(x,y,x_edge,y_edge):
    """使用plt.hist2d计算x和y的相关性矩阵"""
    
    # 筛选异常值
    data = np.vstack((np.array(x),np.array(y))).T
    clf = LocalOutlierFactor(n_neighbors=10)
    predict = clf.fit_predict(data)
    score = clf.negative_outlier_factor_

    # 绘制散点图
    # plt.scatter(x, y, s=20, c=predict, marker='o')
    # plt.show()

    # 计算二维频数
    # h, xedge, yedge, _ = plt.hist2d(x, 
    #                                  y, 
    #                                  bins=[10, 20], 
    #                                  range=[[0, 10], [0, 80]], 
    #                                  cmap='Blues',
    #                                  norm=colors.LogNorm())
    h, xedge, yedge = np.histogram2d(x, 
                                     y, 
                                     bins=[x_edge, y_edge])
    
    # print(h.tolist())
    # print(xedge)
    # print(yedge)

    return h


def main_calculate_txt(isshow=False,issave=True):
    """从TXT格式的的DWS数据计算重量和体积的相关性矩阵并将结果至为csv文件"""
    datapath = 'project/zhuangzailv/data_dws_hefei.txt'
    savedir = 'project/zhuangzailv'
    savename_map = Path(savedir) / '0703_mat.jpg'
    savename_csv = Path(savedir) / '0703_mat.csv'

    x, y = read_data_txt(datapath)

    x_edge = np.array([0,1,2,3,4,5,6,7,8,9,10,40])
    x_label = ['%s-%s'%(x_edge[i], x_edge[i+1]) for i in range(len(x_edge)-1)]
    y_edge = np.array([0,4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64,68,72,76,80,100])
    y_label = ['%s-%s'%(y_edge[i], y_edge[i+1]) for i in range(len(y_edge)-1)]
    y_mid = np.array([2,6,10,14,18,22,26,30,34,38,42,46,50,54,58,62,66,70,74,78,82])
    print('x_edge: %s'%x_edge)
    print('x_label: %s'%x_label)
    print('y_edge: %s'%y_edge)
    print('y_label: %s'%y_label)
    print('y_mid: %s'%y_mid)

    # 计算二维频数矩阵
    # nums = calculate_matrix_own(x,y)
    nums = calculate_matrix_np(x,y,x_edge,y_edge)
    print('len: %s,%s'%nums.shape)

    # 按行标准化
    nums_nor = normalize(nums, axis=1, norm='l1')

    data = []
    i = 0
    for _frequency,_probability in zip(nums,nums_nor):

        y_averages = np.dot(y_mid, _probability.T)

        # 增加数据
        data.append({"x_left": i,
                     "y_average": y_averages,
                     "y_frequency": _frequency.tolist(),
                     "y_probability": _probability.tolist()})
        i = i+1

    csvdata = pd.DataFrame(data)

    # 绘制矩阵图
    plt.matshow(nums_nor, cmap=plt.cm.Reds)
    plt.colorbar()
    plt.title("matrix A")
    if issave:
        plt.savefig(savename_map,dpi=300, bbox_inches='tight')
    if isshow:
        ax = plt.gca()
        ax.xaxis.set_ticks_position('bottom')
        ax.invert_yaxis()
        plt.show()

    # 保存矩阵为csv文件
    if issave:
        csvdata.to_csv(savename_csv)


def calculate_one(x, y, x_edge, y_edge, y_mid):
    """根据已知数据计算一次相关性矩阵
    
    Params
        x, y, x_edge, y_edge, y_mid
    Return
    
    """
    # 统计二位直方图频数
    nums, _, _ = np.histogram2d(x, 
                                y, 
                                bins=[x_edge, y_edge])
    # 按行标准化
    nums_nor = normalize(nums, axis=1, norm='l1')

    # 计算每个重量区间的平均体积
    data = []
    i = 0
    for _frequency,_probability in zip(nums,nums_nor):
        y_averages = np.dot(y_mid, _probability.T)
        y_frequency = _frequency.tostring()
        y_probability = _probability.tostring()
        i += 1
        data.append((i, y_averages, y_frequency, y_probability))

    return data


def main_calculate_mysql():
    """从MySQL的DWS数据表中拉取重量和体积数据计算相关性矩阵并将结果至结果表"""
    # 连接数据库
    dbmysql = DBMySQL()

    # 筛选条件
    ORGS = ['合肥蜀山(23000071)']
    LOCATIONS = ['双层+小件机']
    ROUTERS= ['合肥-芜湖']
    DATES = ['202307']
    
    x_edge = np.array([0,1,2,3,4,5,6,7,8,9,10,40])
    x_label = ['%s-%s'%(x_edge[i], x_edge[i+1]) for i in range(len(x_edge)-1)]
    y_edge = np.array([0,4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64,68,72,76,80,100])
    y_label = ['%s-%s'%(y_edge[i], y_edge[i+1]) for i in range(len(y_edge)-1)]
    y_mid = np.array([2,6,10,14,18,22,26,30,34,38,42,46,50,54,58,62,66,70,74,78,82])

    # 计算相关性数据
    for _org in ORGS:
        for _loc in LOCATIONS:
            for _rout in ROUTERS:
                for _date in DATES:
                    print('%s-%s-%s-%s'%(_org,_loc,_rout,_date))
                    # 查看数据是否存在
                    result = dbmysql.select_result(_org,_loc,_rout,_date)
                    if len(result) > 6:
                        print('× 存在数据已跳过')
                        continue

                    # 拉取DWS数据计算
                    print('√ 开始拉取数据')
                    result = dbmysql.select_weight_volume(_org,_loc,_rout,_date)
                    result_array = np.array(result)
                    x, y = result_array[:,0], result_array[:,1]

                    # 判断数据量是否足够
                    if len(x) < 3000:
                        print('× 数据量%s<3000，跳过'%len(x))
                        continue
                    
                    # 开始计算
                    print('√ 计算相关性矩阵')
                    nums = calculate_matrix_np(x,y,x_edge,y_edge)
                    nums_nor = normalize(nums, axis=1, norm='l1')

                    data = []
                    i = 0
                    for _frequency,_probability in zip(nums,nums_nor):
                        y_averages = np.dot(y_mid, _probability.T)
                        y_frequency = _frequency.tobytes()
                        y_probability = _probability.tobytes()
                        i += 1
                        data.append((_org,_loc,_rout,_date, i, y_averages, y_frequency, y_probability))

                    # 保存至数据库
                    print('√ 计算结果保存至数据库')
                    dbmysql.insert_result(tuple(data))


    # 根据相关性矩阵计算数据
    weightes = [0.9,1.1,2.1]
    we, _ = np.histogram(weightes, bins=x_edge)
    print('重量分布: %s'%we)

    # 拉取计算数据
    result = dbmysql.select_result(_org,_loc,_rout,_date)
    vol = np.array([float(i) for i in np.array(result)[:,1]])
    print('各重量区间平均体积%s'%vol)
    
    try:
        v = np.dot(we, vol)
        print('体积: %s'%v)
    except Exception as e:
        print(e)

def mian_inference_mysql():
    """根据已知数据计算体积"""

    # 统计每个重量区间的频数

    # 每个重量区间的平均体积



def test_read_data_txt():
    x,y = read_data_txt('project/test/data_dws_hefei.txt')
    print('x len: %s, x len: %s'%(len(x), len(y)))


def test_calculate_matrix():
    # 测试相关性矩阵计算
    x = [1.1,1,2.3,3,3,4,5,5,6,6]
    y = [5,5,7,6.7,7,7.5,8,8,8,8]
    savename = 'project/zhuangzailv'
    calculate_matrix_own(x,y,savename)


def test_main(isshow=True,issave=True):
    x = [1.1,1,2.3,3,3,4,5,5,6,6]
    y = [5,5,7,6.7,7,7.5,8,8,8,8]
    savedir = 'project/zhuangzailv/testdata'
    savename_map = Path(savedir) / '0626_mat.jpg'
    savename_csv = Path(savedir) / '0626_mat.csv'

    # 计算二维频数矩阵
    # nums = calculate_matrix_own(x,y)
    nums = calculate_matrix_np(x,y)

    # 按行标准化
    nums_nor = normalize(nums, axis=1, norm='l1')

    # 绘制矩阵图
    plt.matshow(nums_nor, cmap=plt.cm.Reds)
    plt.colorbar()
    plt.title("matrix A")
    if issave:
        plt.savefig(savename_map,dpi=300, bbox_inches='tight')
    if isshow:
        plt.show()

    # 保存矩阵为csv文件
    if issave:
        pd.DataFrame(nums_nor).to_csv(savename_csv)

if __name__=="__main__":
    # test_read_data_txt()
    # test_calculate_matrix()
    # test_main()

    # main_calculate_txt()
    main_calculate_mysql()
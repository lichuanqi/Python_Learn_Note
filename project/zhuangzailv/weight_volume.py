"""研究邮件重量与体积的相关性"""
import sys
import math
from pathlib import Path
from datetime import datetime,timedelta

import numpy as np
import pandas as pd 
from matplotlib import colors
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

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
    
    def select_weight_volume_new(self, 
                                 _org=None, 
                                 _loc=None, 
                                 _rout=None, 
                                 date_start=None,
                                 date_end=None):
        """筛选重量和体积数据

        Params
            _org        : 机构名称
            _loc        : 设备安装位置
            _rout       : 路向
            date_start  : 开始日期
            date_end    : 结束日期

        Return
            x,y
        """
        sql = """SELECT calculate_weight,calculate_volume FROM `zzl_dws_data`"""

        if not all([_org, _loc, _rout, date_start, date_end]):
            return '目前不支持不限制筛选条件'
        
        sql += """ WHERE"""
        if _org is not None:
            sql += """ org_name='%s'"""%_org
        if _loc is not None:
            sql += """ and dws_location='%s'"""%_loc
        if _rout is not None:
            sql += """ and email_router='%s'"""%_rout
        if date_start is not None and date_end is not None:
            sql += """ and collection_time BETWEEN '%s' AND '%s'"""%(date_start,date_end)

        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        if not result:
            return np.array([]), np.array([])

        result_array = np.array(result)
        x, y = result_array[:,0], result_array[:,1]

        return x, y

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


# 连接数据库
dbmysql = DBMySQL()

# 重量体积区间
x_edge = np.array([0,1,2,3,4,5,6,7,8,9,10,40])
x_label = ['%s-%s'%(x_edge[i], x_edge[i+1]) for i in range(len(x_edge)-1)]
y_edge = np.array([0,4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64,68,72,76,80,100])
y_label = ['%s-%s'%(y_edge[i], y_edge[i+1]) for i in range(len(y_edge)-1)]
y_mid = np.array([2,6,10,14,18,22,26,30,34,38,42,46,50,54,58,62,66,70,74,78,82])


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
    
    return np.array(x), np.array(y)


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


def calculate_matrix_np(x,y,x_edge=None,y_edge=None):
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
    if x_edge is None or y_edge is None:
        h, xedge, yedge = np.histogram2d(x,y,range=[[0, 20], [0, 100]])
    else:
        h, xedge, yedge = np.histogram2d(x, 
                                         y,
                                         bins=[x_edge, y_edge],
                                         range=[[0, 20], [0, 100]])
        
    # h, xedge, yedge, _ = plt.hist2d(x, 
    #                                 y, 
    #                                 bins=[10, 20], 
    #                                 range=[[0, 10], [0, 80]], 
    #                                 cmap='Blues',
    #                                 norm=colors.LogNorm())

    return h, xedge, yedge


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


def main_calculate_mysql():
    """从MySQL的DWS数据表中拉取重量和体积数据计算相关性矩阵并将结果至结果表"""
    # 筛选条件
    ORGS = ['合肥蜀山(23000071)']
    LOCATIONS = ['双层+小件机']
    ROUTERS= ['合肥-芜湖']
    DATES = ['202307']
    
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


def main_inference_txt():
    # 根据相关性矩阵计算数据
    org = '合肥蜀山(23000071)'
    loc = '双层+小件机'
    rout= '合肥-芜湖'
    date = '202307'
    weightes = [0.9,1.1,2.1]

    # 统计每个重量区间的频数
    we, _ = np.histogram(weightes, bins=x_edge)
    print('重量分布: %s'%we)

    # 拉取每个重量区间的平均体积
    result = dbmysql.select_result(org, loc, rout, date)
    vol = np.array([float(i) for i in np.array(result)[:,1]])
    print('各重量区间平均体积%s'%vol)
    
    try:
        v = np.dot(we, vol)
        print('体积: %s'%v)
    except Exception as e:
        print(e)


def calculate_one_time(
        w_edge,
        v_edge,
        batch_id,
        date_start,
        date_end,
        _org,
        _loc,
        _rout):
    """计算一次
    
    Params
        w_edge,
        v_edge,
        batch_id,
        date_start,
        date_end,
        _org,
        _loc,
        _rout

    Return

    """
    print('开始计算%s %s %s'%(_org,_loc,_rout))

    # 查看数据是否存在
    result = dbmysql.select_result(_org,_loc,_rout,batch_id)
    if len(result) > 6:
        print('× 存在数据已跳过')
        return

    # 拉取DWS数据计算
    x, y = dbmysql.select_weight_volume_new(_org,_loc,_rout,date_start,date_end)
    if len(x) == 0:
        print('× 未拉取到相关DWS数据')
        return 
    if len(x) < 3000:
        print('× 数据量%s<3000，跳过'%len(x))
        return
    print('√ 拉取数据共%s条'%len(x))
    
    # 开始计算
    nums, xedge, yedge = np.histogram2d(x, 
                                        y,
                                        bins=[w_edge, v_edge])
    nums_nor = normalize(nums, axis=1, norm='l1')
    print('√ 计算相关性矩阵')

    # 保存至数据库
    data = []
    i = 0
    v_mid = v_edge[:-1] + 1
    for _frequency,_probability in zip(nums,nums_nor):
        y_averages = np.dot(v_mid, _probability.T)
        y_frequency = _frequency.tobytes()
        y_probability = _probability.tobytes()
        i += 1
        data.append((_org, _loc, _rout, batch_id, i, y_averages, y_frequency, y_probability))
    dbmysql.insert_result(tuple(data))
    print('√ 计算结果保存至数据库')


def calculate_mysql():
    """从数据库拉取数据计算并将计算结果保存至数据库

    ChangLog
        20230707: 调整计算频数和数据周期
    """
    # 参数
    cal_period = 7                   # 每隔几天计算一次
    cal_length = 28                  # 每次计算使用前几天的数据
    date_start = datetime(2023,7,1)  # 开始日期
    date_end = datetime(2023,7,14)   # 结束日期

    # 重量和体积区间
    w_edge = np.linspace(0, 10, num=50, endpoint=True)
    v_edge = np.linspace(0, 60, num=30, endpoint=True)

    # 根据起止日期计算要计算的批次数
    day_start = (date_start-datetime(date_start.year,1,1)).days + 1         # 开始日期是一年中的第几天
    day_end = (date_end-datetime(date_start.year,1,1)).days + 1             # 结束日期是一年中的第几天
    if day_start%cal_period == 0:                                           # 开始日期的批次数
        batch_start = day_start // cal_period                               
    else:
        batch_start = day_start // cal_period + 1
    if day_end%cal_period == 0:                                             # 结束日期的批次数
        batch_end = day_end // cal_period
    else:
        batch_end = day_end // cal_period + 1
    if batch_end-batch_start <= 0:
        print('起止时间不足一个计算频次')
    print('%s - %s 共需要计算%s批次'%(date_start,date_end,batch_end-batch_start))

    # 逐批次计算
    for batch_index in range(batch_start, batch_end):
        date_end_batch = datetime(date_start.year, 1, 1) + timedelta(days=batch_index*cal_period-1)
        date_start_batch = date_end_batch + timedelta(days=-cal_length)
        batch_id = date_start.year * 100 + batch_index
        print('批次%s: %s - %s'%(batch_id, date_start_batch, date_end_batch))

        # 先从数据库中检索组织机构 设备位置 路向的可选项
        orgs = ['合肥蜀山(23000071)']
        locations = ['双层+小件机']
        routers= ['合肥-芜湖']

        for _org in orgs:
            for _loc in locations:
                for _rout in routers:
                    calculate_one_time(
                        w_edge,
                        v_edge,
                        batch_id,
                        date_start_batch,
                        date_end_batch,
                        _org,
                        _loc,
                        _rout)


def test_calculate_one_time():
    # w_edge = np.linspace(0, 10, num=50, endpoint=True)
    # v_edge = np.linspace(0, 60, num=30, endpoint=True)


    # calculate_one_time(
    #     w_edge,
    #     v_edge,
    #     batch_id,
    #     date_start_batch,
    #     date_end_batch,
    #     _org,
    #     _loc,
    #     _rout)
    pass


def test_main(isshow=True,issave=False):
    """数据分析"""
    # 测试数据
    # x = np.array([1.1,1,2.3,3,3,4,5,5,6,6])
    # y = np.array([5,5,7,6.7,7,7.5,8,8,8,8])
    # 真实数据
    x, y = read_data_txt('project\zhuangzailv\data_dws_hefei.txt')

    print('================== 数据特征分析 ==================')
    print('x shape: %s, y shape: %s'%(x.reshape(-1,1).shape, y.shape))
    
    # 计算pearsonr相关系数
    corr_coef, p_value = pearsonr(x, y)
    print("pearsonr corr_coef: %.4f, p_value: %.4f"%(corr_coef, p_value))
    
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    print('训练集: %s条; 测试集: %s条, 总体积: %.2fL'%(len(X_train), len(X_test), sum(y_test)))

    # 使用随机森林算法预测
    print('================== 随机森林回归预测 ==================')
    model_path = "project/zhuangzailv/random_forest_regression_model.joblib"
    regressor = RandomForestRegressor()
    regressor.fit(X_train.reshape(-1,1), y_train)
    y_pred = regressor.predict(X_test.reshape(-1,1))
    print('拟合度r2 score: %.4f, 预测总体积: %.2f'%(r2_score(y_test, y_pred), sum(y_pred)))

    # 使用相关性概率预测
    print('================== 相关性概率预测 ==================')
    frequency_matrix, xedge, yedge = calculate_matrix_np(X_train, y_train, x_edge, y_edge)
    probability_matrix = normalize(frequency_matrix, axis=1, norm='l1')
    average_volume = np.dot(y_mid, probability_matrix.T)
    print('各重量区间平均体积: %s'%average_volume)

    X_test_hist, _ = np.histogram(X_test, bins=x_edge)
    y_pred = [average_volume[min(int(xx),10)] for xx in X_test]
    y_pred_volume = np.dot(X_test_hist, average_volume)
    print('拟合度r2 score: %.4f, 预测总体积: %.2fL'%((r2_score(y_test, y_pred), y_pred_volume)))

    # savedir = 'project/zhuangzailv/testdata'
    # savename_map = Path(savedir) / '0626_mat.jpg'
    # savename_csv = Path(savedir) / '0626_mat.csv'

    # 计算二维频数矩阵
    # nums = calculate_matrix_own(x,y)
    # nums, xedge, yedge = calculate_matrix_np(x,y)
    # nums, xedge, yedge, _ = plt.hist2d(
    #     x, 
    #     y, 
    #     bins=[10, 40], 
    #     range=[[0, 20], [0, 100]], 
    #     cmap='Blues',
    #     norm=colors.LogNorm())
    # print('xedge: %s'%xedge)
    # print('yedge: %s'%yedge)

    plt.show()

    # 按行标准化
    # nums_nor = normalize(nums, axis=1, norm='l1')

    # # 绘制矩阵图
    # plt.matshow(nums_nor, cmap=plt.cm.Reds)
    # plt.colorbar()
    # plt.title("matrix A")
    # if issave:
    #     plt.savefig(savename_map,dpi=300, bbox_inches='tight')
    # if isshow:
    #     plt.show()

    # # 保存矩阵为csv文件
    # if issave:
    #     pd.DataFrame(nums_nor).to_csv(savename_csv)

if __name__=="__main__":
    # test_read_data_txt()
    # test_calculate_matrix()
    calculate_mysql()
    # test_main()

    # main_calculate_txt()
    # main_calculate_mysql()
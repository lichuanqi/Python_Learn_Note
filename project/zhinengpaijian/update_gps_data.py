from turtle import up, update
import requests
import pandas as pd

from pyecharts.charts import Geo
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.globals import GeoType

# from pyecharts.globals import CurrentConfig
# CurrentConfig.ONLINE_HOST = "https://cdn.jsdelivr.net/npm/echarts@latest/dist/"


class GpsDataset:
    """
    构建GPS数据

    Args
        data_path:
        threshold:
        save_path:
    Output
        
    """
    def __init__(self, data_path, threshold, save_path):
        
        self.data = self.read_data(data_path)
        self.threshold = threshold
        self.save_path = save_path

    def read_data(self, data_path):
        data = pd.read_csv(data_path, header=0, index_col=0)
        # 按照时间排序
        data.sort_values(by='first_xiaduan',inplace=True)
        print(f'读取数据完成, 共 {len(data)} 条')

        return data
    

    def get_gps_by_address(self, address:str):
        """
        使用百度地址正编码api获取地址的gps信息
        Args:
            address: 地址字符串
        Return: 
            gps['lng']: 纬度值
            gps['lat']: 经度值
        """

        ak = '8FCLaF8gdBBufko1tmXN39eUkehVv62M'
        url = 'https://api.map.baidu.com/geocoding/v3/?address=' + address + '&output=json&ak=' + ak

        result = requests.get(url)
        result_json = result.json()

        try:
            gps = result_json['result']['location']
        except :
            print(f'接口返回值异常: {result_json}')
            gps = {'lng': 'error', 'lat': 'error'}

        return gps['lng'],gps['lat']


    def update_gps(self):
        """
        更新GPS数据
        Args
            self.data [DataFrame]:
        
        Return 
            self.data_new [DataFrame]:

        Output
            
        """
        print('开始更新GPS数据...')
        self.data_new = self.data.copy()

        i = 1
        updat_num = 0
        for index, row in self.data.iterrows():
            if i <= self.threshold:
                receiver_addr = row['receiver_addr']
                lng = row['lng']
                lat = row['lat']

                # 根据小数点判断是否存在GPS数据
                if '.' in lng:
                    print(f'{index}, 存在GPS数据: ({lng}, {lat})')

                else:
                    # 只对地址字符串长度在（9，40）之间的地址进行接口调用
                    if len(str(receiver_addr)) >= 9 and len(str(receiver_addr)) <= 50:
                        lng, lat = self.get_gps_by_address(receiver_addr)
                        print(f'{index}: {receiver_addr} -> ({lng}, {lat})')

                        updat_num += 1
                    else:
                        lng, lat = 'pass', 'pass'
                        print(f'{index}: {receiver_addr}, 地址字符串长度不在范围内,跳过')
                
                    self.data_new.loc[index, 'lng'] = lng
                    self.data_new.loc[index, 'lat'] = lat

                # 每运算一部分保存一下
                if i%50 ==0:
                    self.data_new.to_csv(self.save_path,index=True, header=True)
                    print(f'-- SAVE 已保存至：{self.save_path}')

                i += 1

            else:
                self.data_new.to_csv(self.save_path,index=True, header=True)
                print(f'更新结束,共更新 {updat_num} 条数据')
                print(f'-- SAVE 数据已保存至：{self.save_path}')
                break


    def draw_by_gps(self):
        """
        把GPS数据画在地图上
        Args
            self.data [DataFrame]:
        """

        # 绘制地图
        geo=Geo(init_opts=opts.InitOpts(width="1200px",height='600px'))
        geo.set_global_opts(title_opts=opts.TitleOpts(title='育新投递部6.1邮件收件地址分布情况',
                                                    subtitle='数据来源：育新投递明细表'))
        geo.add_schema(maptype='北京')

        gps = []
        for i in range(3000):
            lng = self.data.iloc[i]['lng']
            lat = self.data.iloc[i]['lat']
            leixing = self.data.iloc[i]['business_prodduct_name']

            if '.' in lng:
                gps.append([i, float(lng), float(lat), leixing])
        # print(gps)

        # 新增坐标点
        for g in gps:
            geo.add_coordinate(g[0], g[1], g[2])
        
        # 展示坐标点
        for g in gps:
            geo.add(g[3], [(g[0], 10)], type_=GeoType.SCATTER, symbol_size=6)
        
        # 系列配置项，可配置图元样式、文字样式、标签样式、点线样式等
        geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

        # 输出为html文件
        geo.render('project/zhinengpaijian/geo.html')
        print('已完成')


if __name__ == '__main__':
    data_path = "D:\CPRI\项目6-智能派件\data_gps_1027.csv"
    save_path = "D:\CPRI\项目6-智能派件\data_gps_1028.csv"
    threshold = 7000

    run = GpsDataset(data_path=data_path,
                    threshold=threshold,
                    save_path=save_path)
    # run.update_gps()

    lng, lat = run.get_gps_by_address('北京市海淀区建材城西路育新花园16号')
    print(lng, lat)
    
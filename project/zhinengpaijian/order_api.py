import json
import time
import requests

from pyecharts.charts import Geo
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.globals import GeoType

# from pyecharts.globals import CurrentConfig
# CurrentConfig.ONLINE_HOST = "https://cdn.jsdelivr.net/npm/echarts@latest/dist/"

from main import save_dict2json, json2dict
from isPointinArea import isin_multipolygon


def read_fence():
    """
    生成揽投部基础信息json文件
    """
    path = "D:\CPRI\项目6-智能派件\data_dzwl_yx.txt"

    with open(path, 'r') as f:
        lines = f.readlines()

    lantoubu = {'name': '育新揽投部',
                'loc': [116.351822, 40.062749],
                'fence': []}

    for line in lines:
        ll = line.strip().split(',')
        lng, lat = float(ll[0]), float(ll[1])

        lng_new, lat_new = '%.6f'%lng, '%.6f'%lat

        lantoubu['fence'].append([lng_new, lat_new])

    savename = 'D:\CPRI\项目6-智能派件\data_lantoubu.json'
    save_dict2json(lantoubu, savename)
    print(f'揽投部基础信息保存至: {savename}')


def selecte_orders(orders):
    """
    派件点坐标筛选和去重
    Args
        orders [dict,dict]:
    Return
        orders_new [dict,dict]:
    """
    orders_new = []
    points = []
    area = []
    for i in range(len(lantoubu['fence'])):
        area.append([float(lantoubu['fence'][i][0]), float(lantoubu['fence'][i][1])])

    for order in orders:
        lng, lat = float(order['longitude']), float(order['latitude'])

        point = [float('%.4f'%lng), float('%.4f'%lat)]

        # 去除重复GPS点
        if point not in points:
            points.append(point)

            # 去除电子围栏外的点
            if isin_multipolygon(point, area, contain_boundary=True):
                orders_new.append(order)

    print(f'共 {len(points)}/{len(orders)} 点不重复')
    print(f'共 {len(orders_new)}/{len(orders)} 点在电子围栏中')

    return orders_new


def draw_orders(orders, lantoubu):
    """
    根据orders的经纬度信息把派件点绘制在地图上
    Args
        orders [dict]: 订单经纬度数据
        lantoubu [dict]: 揽投部信息，起始点名称、经纬度数据、电子围栏
                        {
                            "name":"育新揽投部",
                            "loc":[
                                116.351822,
                                40.062749
                            ],
                            "fence":[
                                [
                                    116.416219,
                                    40.059834
                                ],
                                [
                                    116.41532,
                                    40.059226
                                ]
                        }
    """
    # 绘制底图
    geo=Geo(init_opts=opts.InitOpts(width="1200px",height='600px'))
    geo.set_global_opts(title_opts=opts.TitleOpts(title='育新投递部6.1邮件收件地址分布情况',
                                                subtitle='数据来源：育新投递明细表'))
    geo.add_schema(maptype='北京')

    # 绘制揽投部位置
    start_point = [lantoubu['name'], lantoubu['loc'][0], lantoubu['loc'][1]]
    # 新增坐标点
    geo.add_coordinate(start_point[0], start_point[1], start_point[2])
    # 展示坐标点
    geo.add('起始点', [(start_point[0], 5)], type_=GeoType.SCATTER, symbol_size=8)

    # 绘制电子围栏点
    fences = lantoubu['fence']
    for i in range(len(fences)):
        geo.add_coordinate('fence_'+ str(i), fences[i][0], fences[i][1])
    for i in range(len(fences)):
        geo.add('电子围栏', [('fence_'+ str(i), i)], type_=GeoType.SCATTER, symbol_size=8, symbol='triangle')
    
    # 绘制电子围栏点之间的连线
    # for i in range(len(fences)-1):
    #     geo.add('电子围栏', [('fence_'+ str(i), 'fence_'+ str(i+1))], type_=GeoType.LINES)

    # 绘制派件点
    gps = []
    for i in range(len(orders)):
        id = orders[i]['order_id']
        lng = orders[i]['longitude']
        lat = orders[i]['latitude']
        leixing = '速递'

        gps.append([id, lng, lat, leixing])

    for g in gps:
        geo.add_coordinate(g[0], g[1], g[2])

    for g in gps:
        geo.add(g[3], [(g[0], 10)], type_=GeoType.SCATTER, symbol_size=10)

    # 系列配置项，可配置图元样式、文字样式、标签样式、点线样式等
    geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    # 输出为html文件
    savename = 'D:/CPRI/项目6-智能派件/output-1102/order_requests.html'
    geo.render(path=savename)
    print(f'派件点经纬度可视化结果保存至: {savename}')


def request_api(url, orders, start_point):
    """
    请求接口数据

    Args
        url:
        orders:
        start_point: 

    Return

    """

    data_post = {"calc_guid": "112",
        "dept_code": "10009612",
        "route_id": 3,
        "node_name": "育新投递部",
        "one_mail_delivery_duration": 120,
        "work_duration": 240,
        "begin_delivery_time_window": "12:00",
        "end_delivery_time_window": "16:00",
        "vehicle_capacity": 60,
        "max_vehicle_count": 20,
        "nspeed": 20,
        "spent_limit": 1,
        'unimproved_spent_limit': 3600,
        'start_point_lng': start_point[1],
        'start_point_lat': start_point[2],
        "orders": orders}

    start_time = time.time()
    print(f'开始请求接口: {url}')
    try:
        response = requests.post(url=url, json=data_post)
        response_json = response.json()

        end_time = time.time()
        print(f'返回值:\n {response_json}')
        print(f'用时: {end_time-start_time:.4f}')

        # 结果保存为 json 文件
        savename = f'D:/CPRI/项目6-智能派件/output-1028/response_{end_time}.json'
        save_dict2json(response_json, savename)
        print(f'接口返回值已保存至: {savename}')

        return response_json

    except ConnectionError as f:
        print(f'连接错误: {f}')


def chuli_respone_json():
    """
    根据接口返回值提取时间和距离
    """
    respone = {'status': 0, 'message': '成功', 'result': [{'vehicleId': 3, 'dotId': 0, 'arrivetime': 52467, 'departtime': 43200, 'itemnum': 0, 'dealtime': 0, 'dotxlh': 0, 'longitude': 116.351822, 'latitude': 40.062749, 'twindow1': 43200, 'twindow2': 57600}, {'vehicleId': 3, 'dotId': 0, 'arrivetime': 43232, 'departtime': 43352, 'itemnum': 1, 'dealtime': 120, 'dotxlh': 1, 'longitude': 116.352008, 'latitude': 40.062217, 'twindow1': 43200, 'twindow2': 57600}, {'vehicleId': 3, 'dotId': 0, 'arrivetime': 43632, 'departtime': 43752, 'itemnum': 1, 'dealtime': 120, 'dotxlh': 2, 'longitude': 116.356809, 'latitude': 40.059056, 'twindow1': 43200, 'twindow2': 57600}, {'vehicleId': 3, 'dotId': 0, 'arrivetime': 44493, 'departtime': 44613, 'itemnum': 1, 'dealtime': 120, 'dotxlh': 3, 'longitude': 116.342016, 'latitude': 40.065049, 'twindow1': 43200, 'twindow2': 57600}, {'vehicleId': 3, 'dotId': 0, 'arrivetime': 44776, 'departtime': 44896, 'itemnum': 1, 'dealtime': 120, 'dotxlh': 4, 'rrivetime': 48509, 'departtime': 48629, 'itemnum': 1, 'dealtime': 120, 'dotxlh': 10, 'longitude': 116.370406, 'latitude': 40.06081, 'twindow1': 43200, 'twindow2': 57600}, {'vehicleId': 3, 'dotId': 0, 'arrivetime': 48979, 'departtime': 49099, 'itemnum': 1, 'dealtime': 120, 'dotxlh': 11, 'longitude': 116.376398, 'latitude': 40.064756, 'twindow1': 43200, 'twindow2': 57600}, {'vehicleId': 3, 'dotId': 0, 'arrivetime': 49320, 'departtime': 49440, 'itemnum': 1, 'dealtime': 120, 'dotxlh': 12, 'longitude': 116.380348, 'latitude': 40.067101, 'twindow1': 43200, 'twindow2': 57600}, {'vehicleId': 3, 'dotId': 0, 'arrivetime': 50113, 'departtime': 50233, 'itemnum': 1, 'dealtime': 120, 'dotxlh': 13, 'longitude': 116.39271, 'latitude': 40.060331, 'twindow1': 43200, 'twindow2': 57600}, {'vehicleId': 3, 'dotId': 0, 'arrivetime': 50403, 'departtime': 50523, 'itemnum': 1, 'dealtime': 120, 'dotxlh': 14, 'longitude': 116.395697, 'latitude': 40.062167, 'twindow1': 43200, 'twindow2': 57600 }]}

    results = respone.json()['result'][0]

    arrivetime = results['arrivetime']
    departtime = results['departtime']





if __name__=='__main__':

    # TODO: √ 真实数据的经纬度腾讯转百度
    #       √ 根据电子围栏删除异常点
    #       √ 点归集

    orders_json = "D:\CPRI\项目6-智能派件\output-1102\orders.json"
    orders = json2dict(orders_json)['速递_1频']
    
    # 生成揽投部基础信息表
    # read_fence()
    lantoubu_json = 'D:\CPRI\项目6-智能派件\data_lantoubu.json'
    lantoubu = json2dict(lantoubu_json)
    
    start_point = [lantoubu['name'], lantoubu['loc'][0], lantoubu['loc'][1]]
    url_vrp = 'http://132.10.10.41:8001/api/v1/planroutes_one'   # 车辆路径
    url_tsp = 'http://132.10.10.41:8001/api/v1/planroutes'       # 排线

    orders_new = selecte_orders(orders)

    draw_orders(orders_new, lantoubu)
    respone_json = request_api(url, orders_new, start_point)
import sys
import time
import requests

from pyecharts.charts import Geo
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.globals import GeoType

# from pyecharts.globals import CurrentConfig
# CurrentConfig.ONLINE_HOST = "https://cdn.jsdelivr.net/npm/echarts@latest/dist/"

from main import save_dict2json, json2dict
from log import log


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
    logger.info(f'揽投部基础信息保存至: {savename}')


def selecte_orders(orders):
    """
    派件点坐标去重
    Args
        orders [dict,dict]:
    Return
        order_quchong [dict,dict]:
    """
    order_quchong = []
    points = {}

    for i,order in enumerate(orders):

        lng, lat = (float(order['longitude']), float(order['latitude']))
        point = (float('%.5f'%lng), float('%.5f'%lat))
        
        # 判断是否重复
        if point not in points.keys():
            points[point] = len(points)
            order_quchong.append(order)

        else:
            order_quchong[points[point]]['number'] += 1
            order_quchong[points[point]]['transaction_duration'] += 120

    return order_quchong


def draw_orders(orders, lantoubu, savepath) -> None:
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
        num = orders[i]['number']
        leixing = '速递'

        gps.append([id, lng, lat, leixing, num])

    for g in gps:
        geo.add_coordinate(g[0], g[1], g[2])

    for g in gps:
        geo.add(g[3], [(g[0], g[3])], type_=GeoType.SCATTER, symbol_size=10)

    # 系列配置项，可配置图元样式、文字样式、标签样式、点线样式等
    geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    # 输出为html文件
    savename =  savepath + 'order_requests.html'
    geo.render(path=savename)
    logger.info(f'派件点经纬度可视化结果保存至: {savename}')


def request_tsp(orders, savepath):
    """
    请求排线TSP接口,主要用于计算聚合点内部时间

    Args
        orders:

    Return

    """
    url_tsp = 'http://132.10.10.41:8001/api/v1/planroutes_one'       # 排线

    data_post = {"calc_guid": "112",
        "dept_code": "10009612",
        "route_id": 3,
        "node_name": "育新投递部",
        "one_mail_delivery_duration": 120,
        "work_duration": 600,
        "begin_delivery_time_window": "12:00",
        "end_delivery_time_window": "22:00",
        "vehicle_capacity": 60,
        "max_vehicle_count": 20,
        "nspeed": 18,
        "spent_limit": 1,
        'unimproved_spent_limit': 3600,
        'start_point_lng': orders[0]['longitude'],
        'start_point_lat': orders[0]['latitude'],
        "orders": orders}

    logger.debug(f'请求排线TSP接口: {url_tsp}')

    try:
        start_time = time.time()
        response = requests.post(url=url_tsp, json=data_post)
        response_json = response.json()
        end_time = time.time()
        logger.debug(f'接口响应时间: {end_time-start_time:.4f}')

        # 结果保存为 json 文件
        save = {'request': orders, 'response': response_json}
        savename = f'{savepath}request_tsp_{end_time}.json'
        save_dict2json(save, savename)
        logger.debug(f'接口调用值及返回值已保存至: {savename}')

        return response_json

    except ConnectionError as f:
        logger.info(f'连接错误: {f}')


def request_vrp(orders, start_point, savepath):
    """
    请求接口数据

    Args
        url:
        orders:
        start_point: 

    Return

    """

    url_vrp = 'http://132.10.10.41:8001/api/v1/route_calculate/sync'

    data_post = {"calc_guid": "112",
        "dept_code": "10009612",
        "node_name": "育新投递部",
        "one_mail_delivery_duration": 120,
        "work_duration": 360,
        "begin_delivery_time_window": "12:00",
        "end_delivery_time_window": "18:00",
        "vehicle_capacity": 60,
        "max_vehicle_count": 20,
        "nspeed": 20,
        "spent_limit": 1,
        'unimproved_spent_limit': 10,
        'start_point_lng': start_point[1],
        'start_point_lat': start_point[2],
        "orders": orders}

    start_time = time.time()
    logger.info(f'共 {len(orders)} 个点,开始请求排线VRP接口: {url_vrp}')

    try:
        response = requests.post(url=url_vrp, json=data_post)
        response_json = response.json()

        print(response_json)

        end_time = time.time()
        logger.info(f'用时: {end_time-start_time:.4f}')

        # 结果保存为 json 文件
        save = {'request': orders, 'response': response_json}
        savename = f'{savepath}request_vrp_{end_time}.json'
        save_dict2json(save, savename)
        logger.info(f'接口调用值及返回值已保存至: {savename}')

        return response_json

    except ConnectionError as f:
        logger.info(f'连接错误: {f}')


def chuli_respone_tsp(respone):
    """
    根据TSP接口返回值提取行驶时间和投递时间

    Params
        respone [json]: TSP接口返回值
    Return
        time_whole  [int]: 聚合点花费的总时间
        time_xingshi [int]: 行驶时间
        time_toudi [int]: 行驶时间
    """
    results = respone['result']

    # 总时间 = 起始点的到达时间 - 起始点的出发时间
    time_whole = results[0]['arrivetime'] - results[0]['departtime']

    # 逐个获取投递时间
    time_toudi = 0
    for i in range(1, len(results)):
        time_toudi += results[i]['dealtime']

    # 行驶时间 = 总时间 - 投递时间
    time_xingshi = time_whole - time_toudi

    return time_whole, time_xingshi, time_toudi


def chuli_respone_vrp(respone):
    """
    处理VRP接口返回的数据, 提取线路数和每条线路的行驶时间和投递时间
    
    Params
        respone [json]: VRP接口返回值
    Return
        
    """
    ree = []
    time_whole_all, time_xingshi_all, time_toudi_all = 0, 0, 0

    runter_num = 0
    vehicleId_pre = -1

    results = respone['result']
    for i in range(0, len(results)):

        vehicleId = results[i]['vehicleId']
        arrivetime = results[i]['arrivetime']
        departtime = results[i]['departtime']
        dealtime = results[i]['dealtime']

        # 线路编号如果与上一个相同则为同一条线路，累加当前点的投递时间
        # 不相同则为下一条线路的起始点
        if vehicleId == vehicleId_pre:
            time_toudi += dealtime

            if i == len(results)-1:
                time_xingshi = time_whole - time_toudi
                time_whole_all += time_whole
                time_xingshi_all += time_xingshi
                time_toudi_all += time_toudi
                ree.append([time_whole, time_xingshi, time_toudi])

                print(f'第 {runter_num} 条线路, 时间 {time_whole}, '
                    f'总行驶 {time_xingshi}, 总投递时间 {time_toudi}')
        else:
            # 如果不是第一个点就保存上一条线路的信息
            if i != 0:
                time_xingshi = time_whole - time_toudi
                time_whole_all += time_whole
                time_xingshi_all += time_xingshi
                time_toudi_all += time_toudi
                ree.append([time_whole, time_xingshi, time_toudi])

                print(f'第 {runter_num} 条线路, 时间 {time_whole}, '
                    f'总行驶 {time_xingshi}, 总投递时间 {time_toudi}')

            # 如果不是最后一个点就计算下一条线路的时间
            if i != len(results)-1:
                time_whole = arrivetime - departtime
                time_toudi = 0

                runter_num += 1
                vehicleId_pre = vehicleId
    
    # logger.info
    print(f'共 {runter_num} 条线路, 总时间 {time_whole_all}, '
        f'总行驶 {time_xingshi_all}, 总投递时间 {time_toudi_all}')

    return time_whole_all, time_xingshi_all, time_toudi_all


def api_main():
    
    # 生成揽投部基础信息表
    # read_fence()
    lantoubu_json = 'D:\CPRI\项目6-智能派件\data_lantoubu.json'
    lantoubu = json2dict(lantoubu_json)
    start_point = [lantoubu['name'], lantoubu['loc'][0], lantoubu['loc'][1]]

    # 派件点信息
    orders_json = "D:\CPRI\项目6-智能派件\output_1110_wt-60\orders_B.json"
    orders = json2dict(orders_json)

    # 文件保存路径
    savepath = 'D:/CPRI/项目6-智能派件/output_1111_wt-120/'

    # for pin in ['1频', '2频']:

    orders_wai = orders['1频']['整体']
    orders_wai_new = []
    orders_nei = orders['1频']['每个聚合点']
    
    logger.info('TSP 计算聚合点内部行驶时间和投递时间')
    i = 0
    time_xingshi_nei = 0
    time_toudi_nei = 0
    times_nei = []
    for key,value in orders_nei.items(): 
        num = len(value)
        logger.info(f'聚合点{i}: {key}, 派件点数量: {len(value)}')
        
        # 如果聚合点只有一个点只计算投递时间
        if num == 1:
            tt = value[0]['transaction_duration']
            time_whole, time_xingshi, time_toudi = tt, 0, tt
            logger.info(f'总时间 = 投递时间: {time_toudi}s')

        # 派件点数量在 [0,100] 内的调用接口计算
        elif num < 300:
            order_new = selecte_orders(value)
            logger.info(f'派件点去重后剩余: {len(order_new)}')

            # draw_orders(order_new, lantoubu)
            respone_json = request_tsp(order_new, savepath)
            time_whole, time_xingshi, time_toudi = chuli_respone_tsp(respone_json)
            logger.info(f'总时间：{time_whole}, 行驶时间: {time_xingshi}s, 投递时间: {time_toudi}s')

        # 超过300个派件点的聚合点单独一条线路,总时间先按照4小时算
        else: 
            time_xingshi, time_toudi = 6000, 30000
            time_whole = time_xingshi+time_toudi
            logger.info(f'总时间：{time_whole}, 行驶时间: {time_xingshi}s, 投递时间: {time_toudi}s')

        times_nei.append(time_whole)
        
        # 根据聚合点内部数据更新聚合点外部数据
        # 如果单个聚合点的投递时间大于工作时间4小时单独派送
        if time_whole >= 14400:
            pass
        # 
        else:
            order = orders_wai[i]
            order['number'] = num
            order['transaction_duration'] = time_whole

            orders_wai_new.append(order)

        i += 1
    
    logger.info(f'每个聚合点内部的行驶时间和投递时间: {times_nei}')

    # 聚合点内部的数量和时间更新至外部
    orders_update = orders.copy()
    orders_update['1频']['整体'] = orders_wai_new
    savepath_1 = savepath + 'orders_B_update.json'
    save_dict2json(orders_update, savepath_1)
    logger.info(f'orders已更新至: {savepath_1}')

    logger.info('VRP 开始计算外部聚合点之间的行驶时间')
    draw_orders(orders_wai, lantoubu, savepath)
    respone_json = request_vrp(orders_wai, start_point, savepath)

    time_whole, time_xingshi_wai, time_toudi_wai = chuli_respone_vrp(respone_json)

    # 总行驶距离 = 总行驶时间 * 行驶速度
    dis_all_wai = (time_xingshi_wai) * 5

    logger.info(f'总时间: {time_whole/3600:.1f}h,总行驶距离 : {dis_all_wai/1000:.1f}km')


if __name__=='__main__':

    logger = log().get_logger()
    api_main()
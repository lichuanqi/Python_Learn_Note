import time
import requests

from pyecharts.charts import Geo
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.globals import GeoType

# from pyecharts.globals import CurrentConfig
# CurrentConfig.ONLINE_HOST = "https://cdn.jsdelivr.net/npm/echarts@latest/dist/"

from main import save_dict2json
from tomllib import TOMLDecodeError


def draw_orders(orders, start_point):
    """
    根据orders的经纬度信息把派件点绘制在地图上

    Args
        orders [dict]: 订单经纬度数据
        start_point []: 起始点名称及经纬度数据
    """

    # 绘制地图
    geo=Geo(init_opts=opts.InitOpts(width="1200px",height='600px'))
    geo.set_global_opts(title_opts=opts.TitleOpts(title='育新投递部6.1邮件收件地址分布情况',
                                                subtitle='数据来源：育新投递明细表'))
    geo.add_schema(maptype='北京')
    
    gps = []
    for i in range(len(orders)):
        id = orders[i]['order_id']
        lng = orders[i]['longitude']
        lat = orders[i]['latitude']
        leixing = '速递'
        
        gps.append([id, float(lng), float(lat), leixing])

    # 新增坐标点
    geo.add_coordinate(start_point[0], start_point[1], start_point[2])
    for g in gps:
        geo.add_coordinate(g[0], g[1], g[2])

    # 展示坐标点
    geo.add('起始点', [(start_point[0], 5)], type_=GeoType.SCATTER, symbol_size=10)
    for g in gps:
        geo.add(g[3], [(g[0], 10)], type_=GeoType.SCATTER, symbol_size=10)

    # 系列配置项，可配置图元样式、文字样式、标签样式、点线样式等
    geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    # 输出为html文件
    savename = 'project/zhinengpaijian/request.html'
    geo.render(path=savename)
    print(f'派件点经纬度可视化结果保存至: {savename}')


def request_api(url,data_post):
    """
    请求接口数据

    Args
        url:
        data:
    """

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

    except ConnectionError as f:
        print(f'连接错误: {f}')

if __name__=='__main__':

    url = 'http://132.10.10.41:8001/api/v1/planroutes_one'

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
        "nspeed": 9,
        "spent_limit": 1,
        'unimproved_spent_limit': 3600,
        'start_point_lng':'116.35182201204934',
        'start_point_lat':'40.06274904947312',
        # 'end_point_lng':'116.35182201204934',
        # 'end_point_lat':'40.06274904947312',
        "orders": [
        # {
        #     "order_id":18971,
        #     "longitude":"116.33609268256963",
        #     "latitude":"40.06481563685022",
        #     "begin_time":"12:00",
        #     "leave_time":"16:00",
        #     "number":1,
        #     'transaction_duration': 120
        # },
        # {
        #     "order_id":58975,
        #     "longitude":"116.33111032088908",
        #     "latitude":"40.07043354991036",
        #     "begin_time":"12:00",
        #     "leave_time":"16:00",
        #     "number":1,
        #     'transaction_duration': 120
        # },
        # {
        #     "order_id":47352,
        #     "longitude":"116.23761791731043",
        #     "latitude":"40.22641337159427",
        #     "begin_time":"12:00",
        #     "leave_time":"16:00",
        #     "number":1,
        #     'transaction_duration': 120
        # },
        # {
        #     "order_id":17993,
        #     "longitude":"116.36860604202833",
        #     "latitude":"40.069214068668245",
        #     "begin_time":"12:00",
        #     "leave_time":"16:00",
        #     "number":1
        # },
        # {
        #     "order_id":25963,
        #     "longitude":"116.3688693353733",
        #     "latitude":"40.06857522812394",
        #     "begin_time":"12:00",
        #     "leave_time":"16:00",
        #     "number":1
        # },
        # {
        #     "order_id":63859,
        #     "longitude":"116.36860604202833",
        #     "latitude":"40.069214068668245",
        #     "begin_time":"12:00",
        #     "leave_time":"16:00",
        #     "number":1
        # },
        # {
        #     "order_id":35636,
        #     "longitude":"116.37040355135379",
        #     "latitude":"40.06066210483417",
        #     "begin_time":"12:00",
        #     "leave_time":"16:00",
        #     "number":1
        # },
        # {
        #     "order_id":26623,
        #     "longitude":"116.35945796820637",
        #     "latitude":"40.06051507614015",
        #     "begin_time":"12:00",
        #     "leave_time":"16:00",
        #     "number":1
        # },
        # {
        #     "order_id":34408,
        #     "longitude":"116.3702583280781",
        #     "latitude":"40.06475171592352",
        #     "begin_time":"12:00",
        #     "leave_time":"16:00",
        #     "number":1
        # },
        {
            "order_id":72806,
            "longitude":"116.35922045622952",
            "latitude":"40.06789579773766",
            "begin_time":"12:00",
            "leave_time":"16:00",
            "number":1,
            'transaction_duration': 120
        },
        # {
        #     "order_id":39026,
        #     "longitude":"116.35968721577251",
        #     "latitude":"40.06861995268017",
        #     "begin_time":"12:00",
        #     "leave_time":"16:00",
        #     "number":1
        # },
        {
            "order_id":39438,
            "longitude":"116.35678443134756",
            "latitude":"40.06747739663491",
            "begin_time":"12:00",
            "leave_time":"16:00",
            "number":1,
            'transaction_duration': 120
        },
        {
            "order_id":44755,
            "longitude":"116.35925081895577",
            "latitude":"40.07000025664513",
            "begin_time":"12:00",
            "leave_time":"16:00",
            "number":1,
            'transaction_duration': 120
        },
        {
            "order_id":33966,
            "longitude":"116.35968721577251",
            "latitude":"40.06861995268017",
            "begin_time":"12:00",
            "leave_time":"16:00",
            "number":1,
            'transaction_duration': 120
        },
        {
            "order_id":15734,
            "longitude":"116.35933624780976",
            "latitude":"40.06967566447348",
            "begin_time":"12:00",
            "leave_time":"16:00",
            "number":1,
            'transaction_duration': 120
        },
        {
            "order_id":57115,
            "longitude":"116.35668346180825",
            "latitude":"40.06783347256438",
            "begin_time":"12:00",
            "leave_time":"16:00",
            "number":1,
            'transaction_duration': 120
        }
        ]}

    # TODO: 真实数据的经纬度腾讯转百度
    #       根据电子围栏删除异常点
    #       点归集

    orders = data_post['orders']
    start_point = [data_post['node_name'], data_post["start_point_lng"], data_post["start_point_lat"]]

    print(f'共读取到 {len(orders)} 个投递点')

    # draw_orders(orders, start_point)
    request_api(url=url,data_post=data_post)
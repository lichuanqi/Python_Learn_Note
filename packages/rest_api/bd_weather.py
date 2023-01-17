import requests


def api_get_weather_bd():
    """使用百度图获取天气数据

    Params
        district_id: 区县的行政区划编码，和location二选一
        location   : 经纬度，经度在前纬度在后，逗号分隔。
                     支持类型：bd09mc/bd09ll/wgs84/gcj02。开通高级权限后才能使用
        ak         : 开发者密钥，可在API控制台申请获得
        data_type  : 请求数据类型。数据类型有：now/fc/index/alert/fc_hour/all，控制返回内容
        output     : 返回格式，目前支持json/xml
        coordtype  : 支持类型:wgs84/bd09ll/bd09mc/gcj02

    Return:

    """

    api_weather_bd = 'http://api.map.baidu.com/weather/v1/?district_id=222405&data_type=all&ak=8FCLaF8gdBBufko1tmXN39eUkehVv62M'

    data = requests.get(api_weather_bd).json()
    temp = data['result']['now']['temp']

    return temp


if __name__ == '__main__':
    data = api_get_weather_bd()
    print(data)

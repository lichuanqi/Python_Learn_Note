# Python绘制地图神器folium库进行GPS数据的可视化
import folium


orders = [{
            "order_id":"kd_1",
            "longitude":116.38523,
            "latitude":40.05978,
            "begin_time":"12:00",
            "leave_time":"16:00",
            "number":1,
            "transaction_duration":120
        },
        {
            "order_id":"kd_2",
            "longitude":116.37941,
            "latitude":40.06063,
            "begin_time":"12:00",
            "leave_time":"16:00",
            "number":1,
            "transaction_duration":120
        },
        {
            "order_id":"kd_3",
            "longitude":116.38505,
            "latitude":40.0588,
            "begin_time":"12:00",
            "leave_time":"16:00",
            "number":1,
            "transaction_duration":120
        }]

# define the national map
city_map = folium.Map(location=[39.93, 116.40], 
                      zoom_start=10,
                      tiles='openstreetmap')
# save national map
city_map.save('MapVisualization/byfolium.html')

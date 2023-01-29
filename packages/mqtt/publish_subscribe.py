# MQTT客户端订阅主题消息
import json
import random
import time

from paho.mqtt import client as mqtt_client
from paho.mqtt.client import MQTTv5, MQTTMessage


class mqtt_test():
    """MQTT订阅测试"""
    def __init__(self) -> None:
        self.client_id = 'pc_python_0001'
        self.broker = '192.168.1.247'
        self.port = 1883
        self.user = 'lcq'
        self.passward = 'lcq'
        self.topic = "test/enviroment"

        self.connect_mqtt()
        
    def on_connect(client, userdata, flags, rc, reasonCode, properties):
        """建立连接后的回调函数
        
        Params
            flags: 一个包含代理回复的标志的字典
            rc: 连接成功或者不成功
                0-连接成功
                1-协议版本错误
                2-无效的客户端标识
                3-服务器无法使用
                4-错误的用户名或密码
                5-未经授权
        """
        print("Connected with result code: %s"%(rc))

    def on_disconnect(client, userdata, rc):
        """断开连接后的回调函数"""
        print("Disconnection with result code: %d"%(rc))

    def on_subscribe(client, userdata, mid, granted_qos, reasonCode, properties):
        """订阅回调"""
        print("On Subscribed")
    
    def on_unsubscribe(client, userdata, mid, granted_qos):
        """取消订阅回调"""
        print("On unSubscribed: qos = %d" % granted_qos)
        
    def on_message(client, userdata, message, Decorator:MQTTMessage):
        """收到消息后的回调函数"""
        print(f'收到消息: ' + str(Decorator.payload.decode()))

        # TODO: 保存数据

    def on_publish(client, userdata, _, mid):
        """发布消息回调
        
        对于Qos级别为1和2的消息，这意味着已经完成了与代理的握手。
        对于Qos级别为0的消息，这只意味着消息离开了客户端。
        mid变量与从相应的publish()返回的mid变量匹配，以允许跟踪传出的消息。
        """
        print("On onPublish: %s" %(mid))

    def connect_mqtt(self):
        print('开始连接MQTT服务器')
        self.Client = mqtt_client.Client(client_id=self.client_id,
                                         protocol=MQTTv5)
        self.Client.username_pw_set(self.user, self.passward)
        
        # 回调函数
        self.Client.on_connect = self.on_connect
        self.Client.on_disconnect = self.on_disconnect
        self.Client.on_subscribe = self.on_subscribe
        self.Client.on_unsubscribe = self.on_unsubscribe
        self.Client.on_message = self.on_message
        self.Client.on_publish = self.on_publish

        self.Client.connect(self.broker, self.port, 60)

    def start_subscribe(self):
        print(f'开始监听主题: {self.topic}')
        self.Client.subscribe(self.topic)
        self.Client.loop_forever()

    def start_publish(self):
        for i in range(100):
            temp = random.randint(10, 20)
            shidu = random.randint(60, 80)
            data = {"temp": temp, "shidu": shidu}
            msg = json.dumps(data)
            status, msg_id = self.Client.publish(self.topic, msg, qos=0)

            if status == 0:
                print(f'Publish Success, id={msg_id}, msg={msg}')

            time.sleep(5)

if __name__ == '__main__':
    run = mqtt_test()

    # 测试订阅
    run.start_subscribe()

    # 测试发布
    # run.start_publish()
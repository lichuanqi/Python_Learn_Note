# MQTT客户端订阅主题消息
import json
import random
import time

from paho.mqtt import client as mqtt_client
from paho.mqtt.client import MQTTv5, MQTTMessage


class mqtt_test():
    def __init__(self) -> None:
        self.broker = '192.168.35.221'
        self.port = 1883
        self.topic = "test/envirment"
        self.Client_id = 'pc_python_0001'
        
    def on_connect(client, userdata, flags, rc, reasonCode, properties):
        """建立连接后的回调函数"""
        print("Connected with result code "+str(rc))
        
    def on_message(client, userdata, message, Decorator:MQTTMessage):
        """收到消息后的回调函数"""
        print(f'收到消息: ' + str(Decorator.payload.decode()))

        # TODO: 保存数据

    def connect_mqtt(self):
        self.Client = mqtt_client.Client(client_id=self.Client_id,
                                         protocol=MQTTv5)
        self.Client.on_connect = self.on_connect                  
        self.Client.on_message = self.on_message
        self.Client.connect(self.broker, self.port)

    def subscribe(self):
        print(f'开始监听主题: {self.topic}')
        self.Client.subscribe(self.topic)
        self.Client.loop_forever()

    def start_subscribe(self):
        self.connect_mqtt()
        self.subscribe()
        

if __name__ == '__main__':
    run = mqtt_test()
    run.start_subscribe()
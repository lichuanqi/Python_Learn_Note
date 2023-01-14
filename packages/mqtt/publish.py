# MQTT客户端发布消息
import json
import random
import time

from paho.mqtt import client as mqtt_client
from paho.mqtt.client import MQTTv5


class mqtt_test():
    def __init__(self) -> None:
        self.broker = '192.168.35.221'
        self.port = 1883
        self.topic = "test/envirment"
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'

    def connect_mqtt(self):
        self.client = mqtt_client.Client(client_id=self.client_id,
                                         protocol=MQTTv5)
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def publish(self):
        msg_count = 0
        while True:
            temp = random.randint(10, 20)
            shidu = random.randint(60, 80)
            data = {"temp": temp, "shidu": shidu}
            msg = json.dumps(data)
            status, msg_id = self.client.publish(self.topic, msg, qos=0)

            if status == 0:
                print(f'Publish Success, id={msg_id}, msg={msg}')

            msg_count += 1
            time.sleep(5)

    def start_publish(self):
        self.connect_mqtt()
        self.publish()
        

if __name__ == '__main__':
    run = mqtt_test()
    run.start_publish()
from gateway_iot_aws.aws_mqtt import AWSMQTT
import time
import json

class GateWaysNode():
    def __init__(self, clientId):
        self.debug('Init GateWaysNode')
        self.utm_mqtt = AWSMQTT(clientId)
        self.utm_mqtt.setCallbacks(self.mqttCallback) 

    def mqttCallback(self, client, userdata, message):
        str = message.payload
        # self.debug(str)
        try:
            dict = json.loads(str)
            # parse json msg here            
        except:
            self.debug("mqttCallback: Parse json error")

    def config(self):
        self.debug("Configure mqtt")
        self.utm_mqtt = self.utm_mqtt.config()
    
    def start(self):
        self.debug('Start GatewayNode')
        if not self.utm_mqtt.start():
            self.debug('MQTT error')
        
    def listen(self, topic):
        self.utm_mqtt.subscribe(topic)

    def send(self, topic, message):
        self.debug('Sending message')
        if self.utm_mqtt.publish(topic, json.dumps(message)):
            self.debug('Mesage sent')
        else:
            self.debug('Failed to send')

    def debug(self, data):
        print('[GateWaysNode]['+ str(time.time()) + ']: ' +  str(data))        

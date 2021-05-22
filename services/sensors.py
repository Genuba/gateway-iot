import time
import json
from controllers.sensor8266 import Sensor8266
from utils.utils import defaultencode
from decimal import Decimal
from gateway_iot_aws import gate_way

class Sensors:
    def turnOnLightSensor(request):
        print(request)
        gate_way.send("$aws/things/MyESP32/shadow/update",request)
        return {'message': 'hello world post'}

    def updateSensor():
        return Sensor8266.insertData()
        
    def getSensors():
        return json.dumps(Sensor8266.getData(), default=defaultencode)
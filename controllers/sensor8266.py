from controllers import *
import os

__TableName__ = "Sensor8266"
table = DDB.Table(__TableName__)

class Sensor8266:

    def insertData():
        input = {'timeStamp': '2021-10-02','temperature': '50','payload':'{"hello":"hello from four"}'}
        print('Successfully put item')
        return table.put_item(Item=input)

    def getData():
        response = table.scan()
        return response['Items']
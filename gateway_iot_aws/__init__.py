from gateway_iot_aws.gateway_node import GateWaysNode
import os

gate_way = GateWaysNode('getway1')
gate_way.config()
gate_way.start()
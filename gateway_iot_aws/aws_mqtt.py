import time
import boto3
from boto3.session import Session
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from utils.definitions import ROOT_PATH


cognitoIdentityPoolID = 'us-east-1:4f4a1eaa-a365-4455-871b-836d814ba308'
host = "a2k22rlj3fvdub-ats.iot.us-east-1.amazonaws.com"

port = 443
region = 'us-east-1'
rootCAPath = '/gateway_iot_aws/root-ca.pem'

# cognitoIdentityPoolID = 'us-west-2:03a5c970-ea82-4f31-9046-e84391c37180'
# host = 'aak6simcpykjh.iot.us-west-2.amazonaws.com'


class AWSMQTT(AWSIoTMQTTClient):
    def __init__(self, clientId):
        AWSIoTMQTTClient.__init__(self, clientId, useWebsocket=True)
        print ('init AWSMQTT')
        self.clientId = clientId            

    def setCallbacks(self, mqttCallback):
        self.mqttCallback = mqttCallback
        
    def config(self):
        print('Configure MQTT')
        # Cognito auth
        identityPoolID = cognitoIdentityPoolID
        cognitoIdentityClient = boto3.client('cognito-identity', region_name=region)

        temporaryIdentityId = cognitoIdentityClient.get_id(IdentityPoolId=identityPoolID)
        identityID = temporaryIdentityId["IdentityId"]

        temporaryCredentials = cognitoIdentityClient.get_credentials_for_identity(IdentityId=identityID)
        AccessKeyId = temporaryCredentials["Credentials"]["AccessKeyId"]
        SecretKey = temporaryCredentials["Credentials"]["SecretKey"]
        SessionToken = temporaryCredentials["Credentials"]["SessionToken"]

        # AWSIoTMQTTClient configuration
        AWSIoTMQTTClient.configureEndpoint(self, host, port)
        AWSIoTMQTTClient.configureCredentials(self, ROOT_PATH + rootCAPath)
        AWSIoTMQTTClient.configureIAMCredentials(self, AccessKeyId, SecretKey, SessionToken)
        AWSIoTMQTTClient.configureAutoReconnectBackoffTime(self, 1, 32, 20)
        AWSIoTMQTTClient.configureOfflinePublishQueueing(self, -1)  # Infinite offline Publish queueing
        AWSIoTMQTTClient.configureDrainingFrequency(self, 2)  # Draining: 2 Hz
        AWSIoTMQTTClient.configureConnectDisconnectTimeout(self, 10)  # 10 sec
        AWSIoTMQTTClient.configureMQTTOperationTimeout(self, 5)  # 5 sec
        print('Configure MQTT done')
        return self

    def start(self):
        # Connect and subscribe to AWS IoT
        try:
            if AWSIoTMQTTClient.connect(self) == True:
                print("Connected to MQTT broker")
                time.sleep(2)
                return True
            else:
                print('Connection failed')
                return False
        except:
            print('Connection error')
            

    def subscribe(self, topic):
        return AWSIoTMQTTClient.subscribe(self, topic, 1, self.mqttCallback)

    def publish(self, topic, message):
        return AWSIoTMQTTClient.publish(self, topic, message, 1)
from flask import Flask, jsonify, request
from functools import wraps
from flask_cors import CORS 
from services.sensors import Sensors
from decode_verify_jwt import lambda_handler

app = Flask(__name__)
CORS(app)

def check_for_token(func):
    @wraps(func)
    def wrapped(*args,**kwargs):
        token = request.headers.get('Authorization')
        event = {'token': token}
        claims = lambda_handler(event, None)
        if claims:
            return func(*args,**kwargs)
        else:
            return jsonify({'message':'Missing token'}), 403
    return wrapped

@app.route('/api/sensors',methods = ['POST','PUT','GET'])
@check_for_token
def sensors():
    print('here')
    if request.method == 'POST':
        return Sensors.turnOnLightSensor(request.get_json())
    elif request.method == 'PUT':
        return Sensors.updateSensor()
    elif request.method == 'GET':
        return Sensors.getSensors()

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
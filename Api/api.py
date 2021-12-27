from os import access
from flask import Flask, abort, jsonify, request, make_response, send_from_directory, json
import jsons
from flask.templating import render_template
from db_accessor import DbAccessor



app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Scripts/<path:path>')
def send_js(path):
    return send_from_directory('Scripts', path)

@app.route('/Content/<path:path>')
def send_content(path):
    return send_from_directory('Content', path)

@app.route('/newpatient', methods=['GET'])
def NewPatient():
    accessor = DbAccessor()
    patinent_ID = accessor.add_patient()
    response = patinent_ID
    return jsonify({'response': response}), 200

@app.route('/checkpatientsessions/<patientId>', methods=['GET'])
def CheckPatientSessions(patientId=0):
    accessor = DbAccessor()
    timer = accessor.getSessionTimer(patientId)
    session_number = accessor.getSessionCount(patientId)
    if session_number < 6 and timer:
        return jsonify({'response': True}), 200
    else:
        return jsonify({'response': False}), 200

class Cards:
    def __init__(self):
        self.set1 = ['I1K', 'I2S', 'I3P', 'I4D', 'I5H', 'I6E', 'I7M', 'I8Hy']
        self.set2 = ['II1Hy', 'II2M', 'II3E', 'II4H', 'II5D', 'II6P', 'II7S', 'II8K']
        self.set3 = ['III1H', 'III2E', 'III3S', 'III4M', 'III5K', 'III6D', 'III7Hy', 'III8P']
        self.set4 = ['IV1P', 'IV2Hy', 'IV3D', 'IV4K', 'IV5M', 'IV6S', 'IV7E', 'IV8H']
        self.set5 = ['V1E', 'V2D', 'V3Hy', 'V4P', 'V5S', 'V6K', 'V7H', 'V8M']
        self.set6 = ['VI1M', 'VI2H', 'VI3K', 'VI4S', 'VI5P', 'VI6Hy', 'VI7D', 'VI8E']

@app.route('/getseries', methods=['GET'])
def GetSeries():
    cards = Cards()
    response = app.response_class(
        response = jsons.dumps(cards),
        status = 200,
        mimetype = 'application/json')
    return response

@app.route('/saveresults', methods=['POST'])
def SaveResults():
    if not request.json:
        abort(400)
    array = json.dumps(request.json)
    ResultsDictionary = json.loads(array)
    print(ResultsDictionary)
    patient_ID = ResultsDictionary['patientId']
    cardsDictionary = ResultsDictionary['cards']
    selectionValues = cardsDictionary.values()
    accessor = DbAccessor()
    session_id = accessor.add_session(list(selectionValues), patient_ID)
    accessor.calc_int_result(cardsDictionary, session_id)
    return jsonify({'response': 'OK'}), 200



if __name__ == '__main__':
    app.run(port=33507, debug=True)
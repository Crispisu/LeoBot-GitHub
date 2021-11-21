from flask import Flask, abort, jsonify, request, make_response, send_from_directory
from flask.templating import render_template


app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Scripts/<path:path>')
def send_js(path):
    return send_from_directory('Scripts', path)

@app.route('/leobot/chat', methods=['POST'])
def ChatWithBot():
    if not request.json:
        abort(400)
    response = "I have no brain yet. RIP"
    return jsonify({'response': response}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=56001, debug=True)
from flask import Flask
from flask import abort
from flask import request
from Thingsspeak import Thingsspeak

app = Flask(__name__)
thingsspeak = Thingsspeak()

@app.route("/log", methods=['POST'])
def control():
    try:
        data = request.json
        print("log: {}".format(data))
        thingsspeak.send(data)
    except Exception as e:
        print(e)
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)

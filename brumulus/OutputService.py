from flask import Flask
from flask import abort
import EnergenieOutput as so
import ProtectedOutput as po


app = Flask(__name__)

outputs = [po.ProtectedOutput(so.EnergenieOutput(1), min_state_time=10)]


@app.route("/output/<int:index>/<string:state>", methods=['GET', 'POST'])
def post(index, state):
    try:
        return outputs[index].set_state(state)
    except Exception as e:
        print(e)
        abort(404)


@app.route("/output/<int:index>/", methods=['GET'])
def get(index):
    try:
        print('index: {}'.format(index))
        return outputs[index].get_state()
    except Exception as e:
        print(e)
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)

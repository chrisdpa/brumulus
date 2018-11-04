from flask import Flask
from flask import abort
from flask import request
import TemperatureControl as tc


app = Flask(__name__)


@app.route("/control/")
def control():
    try:
        current_temp = request.args.get('current_temp', type=float)
        target_temp = request.args.get('target_temp', type=float)
        delta_temp_c = request.args.get('delta_temp_c', type=float)
        delta_time_ms = request.args.get('delta_time_ms', type=int)
        return str(tc.get_output(current_temp, target_temp, delta_temp_c, delta_time_ms))
    except Exception as e:
        print(e)
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

from flask import Flask
from flask import abort
from flask import request
import StringOutput
import ControlledOutput
import ProtectedOutput


app = Flask(__name__)

output = ProtectedOutput(StringOutput(), 'Output1')


@app.route("/output/")
def control():
    print('here')
    try:
        print('b')
        return str(tc.get_output(current_temp, target_temp, delta_temp_c, delta_time_ms))
    except Exception as e:
        print(e)
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)

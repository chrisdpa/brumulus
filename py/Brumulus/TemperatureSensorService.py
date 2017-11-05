from flask import Flask
from flask import abort
import TemperatureSensor

app = Flask(__name__)
temperatureSensor = TemperatureSensor.TemperatureSensor()


@app.route("/temp/<int:index>")
@app.route("/temp")
def temp(index=0):
    try:
        return temperatureSensor.read_temp_string(index)
    except Exception as e:
        print(e)
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

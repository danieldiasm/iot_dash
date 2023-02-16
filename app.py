from flask import Flask, render_template, jsonify, request
from flask import url_for

# Constants
DEBUG = False

app = Flask(__name__)


def valid_iot_request(request):
    properties = ['device', 'device_type', 'value_type', 'value_reading']
    valid = 0

    for prop in properties:
        if request.form[prop]:
            print(f'found: {prop}')
            valid += 1

    if len(properties) == valid:
        return True
    return False


@app.route("/", methods=['GET'])
@app.route("/<uname>", methods=['GET'])
def index(uname=None):
    print(uname)
    return render_template('index.html', uname=uname)


@app.route("/about")
def about():
    return "about"


@app.route("/iot")
def iot():
    return jsonify(hello='world')


@app.route("/iot/plant_water/", methods=['POST'])
def iot_plant_water_post():
    error = None
    if request.method == 'POST':
        print(request.form)
        if valid_iot_request(request):
            if int(request.form['value_reading']) < 40:
                return jsonify(water='True')
            return jsonify(water='False')
        return jsonify(success='False')


@app.route("/iot/plant_water/<humidity_lvl>", methods=['GET'])
def iot_plant_water_get(humidity_lvl):
    print(humidity_lvl)
    return jsonify(action=False, got=humidity_lvl), 200


with app.test_request_context():
    print(url_for('index'))

if __name__ == "__main__":
    app.run(host='192.168.50.17', port=8080, debug=DEBUG)

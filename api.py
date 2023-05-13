from flask import Flask, request, jsonify
from main import *

app = Flask(__name__)


@app.route('/api', methods=['POST'])
def api():
    code = request.data.decode('utf-8')
    simulator = Simulator()
    simulator.saveTextToFile(code)
    simulator.setMemory()
    simulator.storeCodeAtAddress(2000)
    return jsonify({"reg": get_hex_register_value(registers),  "flags": flags, "mem": memory})


if __name__ == '__main__':
    app.run(debug=True)

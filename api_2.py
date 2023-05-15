from flask import Flask, request, jsonify
from newmain import *
simulatorobj = Simulator()
app = Flask(__name__)

# api to set memory
@app.route('/read_code', methods=['POST'])
def read_code():
    data = request.data.decode('utf-8')
    simulatorobj=Simulator()
    simulatorobj.saveData(data)
    return jsonify({'message': registers})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
import warnings
warnings.filterwarnings("ignore")
# import numpy as np
import pickle
import sklearn

model = pickle.load(open('Selected_kmeans.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return 'hello world'

@app.route('/pred', methods=['POST'])
def predict():
    acc_x = request.form.get('acc_x')
    acc_y = request.form.get('acc_y')
    acc_z = request.form.get('acc_z')
    magnitude = request.form.get('magnitude')
    motion = request.form.get('motion')
    BPM = request.form.get('BPM')

    if motion == 'walking':
        motion = 4
    elif motion == 'movement':
        motion = 0
    elif motion == 'running':
        motion = 1
    elif motion == 'steady':
        motion = 2
    else:
        motion = 3

    acc_x = float(acc_x)
    acc_y = float(acc_y)
    acc_z = float(acc_z)
    magnitude = float(magnitude)
    BPM = int(BPM)

    inputData = [[acc_x, acc_y, acc_z, magnitude, motion, BPM]]
    stress = model.predict(inputData)[0]

    if (stress == 0):
        raga = 'High Stress'
    elif (stress == 1):
        raga = 'Normal Stress'
    else:
        raga = 'Low Stress'

    return jsonify({'Stress level': str(stress), 'Stress type': raga})


if __name__ == '__main__':
    app.run(debug=True)
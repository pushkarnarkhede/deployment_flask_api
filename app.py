from flask import Flask, request, jsonify
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pickle
import random

model = pickle.load(open('Selected_kmeans.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return 'hello world'

@app.route('/pred', methods=['POST'])
def predict():
    acc_x = float(request.form.get('acc_x'))
    acc_y = float(request.form.get('acc_y'))
    acc_z = float(request.form.get('acc_z'))

    magnitude = np.sqrt(((acc_x)** 2) + ((acc_y)** 2) + ((acc_z)** 2))

    motion = 2 if 0.2 < magnitude < 0.5 else \
             0 if 0.5 < magnitude < 1.0 else \
             4 if 1.0 < magnitude < 1.7 else \
             1 if magnitude > 1.7 else \
             3

    ranges = {
        2: (60, 90),
        4: (80, 136),
        0: (70, 113),
        1: (100, 157),
        3: (60, 157)
    }

    if motion in ranges:
        lower, upper = ranges[motion]
        BPM = int(random.randint(lower, upper))
    else:
        BPM = int(random.randint(60, 157))

    print(magnitude)
    print(motion)
    print(BPM)

    inputData = [[acc_x, acc_y, acc_z, magnitude, motion, BPM]]
    stress = model.predict(inputData)[0]

    raga = 'High Stress' if stress == 0 else \
           'Normal Stress' if stress == 1 else \
           'Low Stress'

    return jsonify({'Stress level': str(stress), 'Stress type': raga})


if __name__ == '__main__':
    app.run(debug=True)
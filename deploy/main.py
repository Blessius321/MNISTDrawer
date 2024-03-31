from flask import Flask, render_template, request, jsonify
from PIL import Image
import io, base64
import numpy as np
import model
app = Flask(__name__)

@app.route('/')
def hello():
    print('hello')
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def predict():
    data = request.get_json()
    raw_image = str(data['image'])
    base64Image = raw_image.split(',')[1]
    img = Image.open(io.BytesIO(base64.b64decode(base64Image))).convert('L').resize((28,28), Image.Resampling.LANCZOS)
    pred = model.predict(img)
    return jsonify(prediction=pred)

if __name__ == "__main__":
         app.run(host='0.0.0.0')

from flask import Flask, render_template, request
from model import get_tensor, prediction, get_model
import os

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route("/result", methods = ["POST"])
def result():
    target = os.path.join(APP_ROOT, "static/")
    if not os.path.isdir(target):
        os.mkdir(target) 
    for file in request.files.getlist('file'):
        filename = file.filename
        print(filename)
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
    model = get_model()
    prob, breed = prediction(model, file)
    return render_template('result.html', image_name = filename, breed = breed, probability = prob)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, Response, render_template
import pickle
from prediction.predict import transformData
import os

app = Flask(__name__)
# list_params = ["watch-model", "case-material", "strap-type", "dial-type", "case-size"]
# make a directory to store images that will be rendered to browser
imageFolder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = imageFolder

@app.route("/", methods=['GET'])
def index():
    return render_template('submission-form.html')

@app.route("/results", methods=['POST'])
def output_quote():
    quote = request.form
    print(quote)
    print("Watch: ", quote['watch-model'])
    # Need to grab values from submission form and map throught them to send through model
    # For radio buttons, it assigns 1 to correct value, but you need to programmatically set other values to 0
    # reformat into dataframe row and make prediction
    prediction = transformData(quote)

    # get feature images to render in html
    featureGraph = os.path.join(app.config['UPLOAD_FOLDER'], 'featureGraph.png')

    return render_template('quote.html', prediction=prediction, watchName=quote['watch-model'], featureGraph=featureGraph)

if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
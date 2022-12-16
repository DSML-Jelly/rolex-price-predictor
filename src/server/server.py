from flask import Flask, request, jsonify, Response, render_template
import pickle
from prediction.predict import transformData


app = Flask(__name__)
list_params = ["watch-model", "case-material", "strap-type", "dial-type", "case-size"]


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

    return render_template('quote.html', prediction=prediction, watchName=quote['watch-model'])

if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
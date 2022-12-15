from flask import Flask, request, jsonify, Response, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('src/watches_lgbm_initial_model.pkl', 'rb'))
list_params = ["watch-model", "case-material", "strap-type", "dial-type", "case-size"]


@app.route("/", methods=['GET'])
def index():
    return render_template('submission-form.html')

@app.route("/results", methods=['POST'])
def output_quote():
    quote = request.form
    # Need to grab values from submission form and map throught them to send through model
    # For radio buttons, it assigns 1 to correct value, but you need to programmatically set other values to 0
    return render_template('quote.html')

if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
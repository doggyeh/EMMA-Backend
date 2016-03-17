#!flask/bin/python

"""RESTful service to communicate with mobile app."""

from flask import Flask, jsonify, abort, request
from questions import init, get_model, list_feature

app = Flask(__name__)

init_value = init()
m = get_model()

@app.route('/api/v1.0/query', methods=['POST'])
def query():
    question = request.json['question']
    answer = list_feature(question.replace(' ', ''), init_value, m, False)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)

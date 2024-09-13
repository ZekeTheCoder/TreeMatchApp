#!/usr/bin/env python3
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return jsonify('Hello, Welcome to TreeMatch!')


@app.route('/api/users', methods=['GET'])
def users():
    return jsonify({"users": ['Thabang', 'Zeke', 'The Coder']})


if __name__ == '__main__':
    app.run(debug=True, port=5000)

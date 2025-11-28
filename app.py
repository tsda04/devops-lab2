#!/usr/bin/env python3
from flask import Flask
import datetime
import os

app = Flask(__name__)

@app.route('/')
def health():
    return {'status': 'healthy1234', 'timestamp': datetime.datetime.now().isoformat()}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=False)

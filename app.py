from flask import Flask , request
import pandas as pd
import numpy as np
import json

import os



APP = Flask(__name__)





@APP.route('/')
def hello_world():
    dict1 = {'TA': {'sell':0.5,'hold':0.25,'buy':0.25}, 'Sentiment':{'sell':0.5,'hold':0.25,'buy':0.25}}
    json1 = json.dumps(dict1)
    response=json1
    print(response)


    return response

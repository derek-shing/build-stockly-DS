from flask import Flask , request
import pandas as pd
import numpy as np

import os



APP = Flask(__name__)





@APP.route('/')

def hello_world():

    response='HelloWorld'
    print(response)


    return response

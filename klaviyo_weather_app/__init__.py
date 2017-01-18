import flask
import redis
import smtplib
from flask import Flask, request, render_template

# Make the redis connection (make sure redis is running first!)
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

# Initialize the flask app
app = Flask(__name__)

# Import the views
# NOTE: this is a circular import but because we don't do anything in this file
# after we import it should be fine. There are solutions to this, but they're not
# necessary until the application needs to scale
import klaviyo_weather_app.register
import klaviyo_weather_app.weather

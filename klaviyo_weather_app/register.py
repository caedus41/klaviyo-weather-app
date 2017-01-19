import re

from flask import jsonify, make_response, render_template, request

from klaviyo_weather_app import redis, application
from klaviyo_weather_app import cities


EMAIL_RE = '^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*'\
           '@[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})$'


class UserExistsException(Exception):
    pass


@application.route('/', methods=['GET'])
def get():
    try:
        return render_template('register.html', cities=[c[1] for c in cities.cities])
    except Exception as e:
        print e


@application.route('/', methods=['POST'])
def post():
        try:
            # Get email from form and validate it
            email = request.form.get('email_addr')
            if re.match(EMAIL_RE, email) is None:
                return make_response('Invalid email address entered', 400)
            # Location selected from a list, doesn't require validation
            location = request.form.get('location')
            # Add email to redis db, erroring out and redirecting if it's already present
            _add_email_to_redis(email, location)
        except UserExistsException as uee:
            print uee
            return make_response(render_template('user_exists.html'), 403)
        except Exception as e:
            print e

        return jsonify('Successfully registered')

def _add_email_to_redis(email, location):
    if email not in redis.hkeys('emails'):
        redis.hset('emails', email, location)
    else:
        raise UserExistsException

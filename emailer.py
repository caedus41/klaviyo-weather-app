import email
import smtplib
import jinja2

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, PackageLoader

import klaviyo_weather_app
from klaviyo_weather_app import cities, redis
from klaviyo_weather_app.weather import *


SENDER = u'klaviyotestemail@gmail.com'


def email_the_users():
    data = redis.hgetall('emails')
    try:
        for email_addr in data.iterkeys():
            print 'Starting email %s' % email_addr
            entered_location = data[email_addr]
            location = [c[0] for c in cities.cities if c[1] == entered_location].pop()
            if not location:
                raise TypeError('Invalid location entered')
            curr_temp = get_curr_temp(location)
            avg_temp = get_avg_temp(location)
            rain = is_raining(location)
            weather = get_curr_weather(location)
            if curr_temp < (avg_temp - 5) or rain:
                subject = "Not so nice out? Enjoy a discount on us."
                template = env.get_template('bad_weather.html')
                print "Rendering bad template"
                body = template.render(
                    location=entered_location,
                    temperature=curr_temp,
                    weather=weather
                )
            elif curr_temp > (avg_temp + 5):
                subject = "It's nice out! Enjoy a discount on us."
                template = env.get_template('good_weather.html')
                print "Rendering good template"
                body = template.render(
                    location=entered_location,
                    temperature=curr_temp,
                    weather=weather
                )
            else:
                subject = "Enjoy a discount on us."
                template = env.get_template('normal_weather.html')
                print "Rendering template"
                body = template.render(
                    location=entered_location,
                    temperature=curr_temp,
                    weather=weather
                )

            msg = MIMEMultipart('alternative')
            msg.attach(body)
            msg['Subject'] = subject
            msg['From'] = SENDER
            msg['To'] = email_addr
            print 'Emailing %s' % email_addr
            smtp_conn.sendmail(SENDER, email_addr, body)
    except Exception as e:
        print e
        pass

    smtp_conn.quit()

if __name__ == "__main__":
    # Set up the template renderer
    env = Environment(loader=PackageLoader('klaviyo_weather_app', 'templates'))

    # Make the smtp connection
    smtp_conn = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_conn.ehlo()
    smtp_conn.login('klaviyotestemail@gmail.com', 'cDj9fY8wQG')
    # Send the emails
    email_the_users()


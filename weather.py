import json
import urllib2
from datetime import date


API_URL = 'http://api.wunderground.com/api/3fcb142cb0311407/%s/q/%s.json'
# features, query


#TODO: *args here?
def _query_api(features, query):
    """ Query the Wunderground API

    :param features: The Wunderground data feature you'd like to access
    :param query: The location you'd like to query
    :return: The json returned by the API
    """
    url = API_URL % (features, query)
    # TODO: try-catch
    f = urllib2.urlopen(url)
    js = json.loads(f.read())
    return js


def get_curr_temp(location):
    """ Gets current temperature at given location

    :param location: pytz.location: the location where you'd like to know the weather
    :return: the weather at the requested location
    """
    data = _query_api('conditions', location)
    curr_temp = data['current_observation']['temp_f']
    curr_feel = data['current_observation']['feelslike_f']
    return curr_temp, curr_feel


def get_avg_temp(location):
    """ Gets the average temperature at this time of the year for the given location

    :param location: pytz.location: the location where you'd like to know the weather
    :paramt dt: datetime object of the time of year you want the average for
    :return: the average temperature in degrees F at the given location for the given time
    """
    'YYYY_MMDD'

    today = date.today()
    query = 'history_%s_%s%s' % (today.year, today.month, today.day)
    data = _query_api(query, location)
    meantemp = data['history']['dailysummary'][0]['meantempi']
    return meantemp


def is_raining(location):
    """ Determine whether or not it will rain today at the given location

    :param location: pytz.location: the location where you'd like to know the weather
    :return: boolean corresponding to whether or not it is raining at the locatino
    """
    data = _query_api('conditions', location)
    precip_today = data['current_observation']['precip_today_string']
    return precip_today


def get_current_weather(location):
    """ Determine the weather in the given location

    :param location: pytz.location: the location where you'd like to know the weather
    :return: boolean corresponding to whether or not it is raining at the locatino
    """
    data = _query_api('conditions', location)
    weather = data['current_observation']['weather']
    return weather

"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
from pprint import pformat
from geopy.geocoders import Nominatim
import requests


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_ask_permissions_response(title, output, reprompt_text, should_end_session):
    response = build_speechlet_response(title, output, reprompt_text, should_end_session)
    response['card'] = {
        'type': 'AskForPermissionsConsent',
        'permissions': ['read::alexa:device:all:address:country_and_postal_code']
    }
    return response


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def get_parish_output(parish):
    church_worship_times = parish['church_worship_times']
    weekend = filter(lambda x: x['service_typename'] == "Weekend", church_worship_times)
    mass_times = " and ".join("%s at %s" % (w['day_of_week'], w['time_start']) for w in weekend)
    if len(weekend) > 1:
        output = "The weekend masses for %s are %s" % (parish['name'], mass_times)
    elif len(weekend) == 1:
        output = "The weekend mass for %s is %s" % (parish['name'], mass_times)
    else:
        output = "There are no weekend masses at %s" % (parish['name'])
    return output
                              

def build_parish_response(parishes):
    if len(parishes) == 1:
        title = "1 parish found"
    elif len(parishes) == 30:
        title = "At least 30 parishes found"
    else:
        title = "%d parishes found" % len(parishes)

    output = "Here are the mass times for the closest parish. %s" % get_parish_output(parishes[0])
    reprompt_text = output
    should_end_session = True
    session_attributes = {}
    return build_response(session_attributes,
                          build_speechlet_response(title,
                                                   output,
                                                   reprompt_text,
                                                   should_end_session))


def build_no_results_response():
    title = "No parishes found"
    output = "I'm sorry, but I couldn't find any parishes"
    reprompt_text = output
    should_end_session = True
    session_attributes = {}
    return build_response(session_attributes,
                          build_speechlet_response(title,
                                                   output,
                                                   reprompt_text,
                                                   should_end_session))


def build_get_consent_request():
    title = "Location consent needed"
    output = "In order to provide information on parishes near you, please grant location permissions to this skill via the Alexa companion app."
    reprompt_text = output
    should_end_session = True
    session_attributes = {}
    return build_response(session_attributes,
                          build_ask_permissions_response(title,
                                                         output,
                                                         reprompt_text,
                                                         should_end_session))


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    reprompt_text = "Please ask me for mass times near you or for a certain day"
    speech_output = "Welcome to Mass Times. " + reprompt_text
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using Mass Times. " \
                    "Have a blessed day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite color is " + favorite_color + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "You can say, my favorite color is red."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def get_consent_token(event):
    return event.get('context', {}) \
                .get('System', {}) \
                .get('user', {}) \
                .get('permissions', {}) \
                .get('consentToken', None)


def get_device_id(event):
    return event.get('context', {}) \
                .get('System', {}) \
                .get('device', {}) \
                .get('deviceId', None)


def on_launch(event):
    """ Called when the user launches the skill without specifying what they
    want
    """

    launch_request, session = event['request'], event['session']
    print(pformat(event))
    context = event['context']['System']
    consent = get_consent_token(event)
    deviceId = get_device_id(event)
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'] +
          ", consent=" + (consent or 'None') +
          ", device=Id" + (deviceId or 'None'))
    # Dispatch to your skill's launch
    return get_welcome_response()


def __print_info(intent, session):
    print("session: " + pformat(session))
    print("intent: " + pformat(intent))


def get_slot_value(intent, name):
    return intent.get('slots', {}).get(name, {}).get('value', None)


def get_parishes_by_lat_lon(latitude, longitude):
    r = requests.get("http://apiv4.updateparishdata.org/Churchs/?lat=%f&long=%f&pg=1"
                     % (latitude, longitude))
    parishes = r.json()
    return parishes


def get_mass_time(event):
    session = event['session']
    intent = event['request']['intent']
    print("get_mass_time")
    __print_info(intent, session)
    city = get_slot_value(intent, 'City')
    address = get_slot_value(intent, 'Address')
    if city is not None:
        geolocator = Nominatim()
        location = geolocator.geocode(city)
        print((location.latitude, location.longitude))
        parishes = parishes_by_lat_lon = get_parishes_by_lat_lon(
            location.latitude, location.longitude)
        if parishes:
            return build_parish_response(parishes)
    if address is not None:
        geolocator = Nominatim()
        location = geolocator.geocode(address)
        print((location.latitude, location.longitude))
        parishes = parishes_by_lat_lon = get_parishes_by_lat_lon(
            location.latitude, location.longitude)
        if parishes:
            return build_parish_response(parishes)
    deviceId = get_device_id(event)
    consent = get_consent_token(event)
    if not (deviceId and consent):
        return build_get_consent_request()
    return build_no_results_response()


def get_parish(intent, session):
    print("get_parish")
    __print_info(intent, session)


def on_intent(event):
    """ Called when the user specifies an intent for this skill """

    intent_request, session = event['request'], event['session']
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetMassTime":
        return get_mass_time(event)
    if intent_name == "GetParish":
        return get_parish(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.5559b95f-aade-4bad-8737-15f28ee7156e"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


if __name__ == '__main__':
    intent = {
      "name": "GetMassTime",
      "slots": {
        "Address": {
          "name": "Address"
        },
        "City": {
          "name": "City"
        },
        "Day": {
          "name": "Day"
        },
        "Date": {
          "name": "Date"
        }
      }
    }
    session = {
        "sessionId": "SessionId.d8e12024-f4dc-43db-aeb7-5fa054163b50",
        "application": {
          "applicationId": "amzn1.ask.skill.5559b95f-aade-4bad-8737-15f28ee7156e"
        },
        "attributes": {},
        "user": {
            "permissions": {},
            "userId": "amzn1.ask.account.AGDQ5OWCX3SNLAS4643LKDQQXZDNXFGEA2ORQY6UCMEED2HALYMNQDRON3QIUCEINM4FXSCCJTCBTTU5INC5G3HO4FIYZX6NOE34QGADWD4OS5T7EILBTQGE4BFLQTG4F26EM6RV4HWSDUBUEUPFFQPS27QAWZZGZZJHNBPE26YEMAO43DF65ICVSWD3W4JIUCODQ4SU4CRUJRQ"
        },
        "new": True
    }
    event = {'request': {'intent': intent},
             'session': session}
    print(pformat(get_mass_time(event)))


import twilio
import twilio.rest
import os

print os.environ.get('TWILIO_ACCOUNT_SID')

try:
    client = twilio.rest.TwilioRestClient(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN') )

    message = client.messages.create(
        body="Hello World",
        to="+19085077420",
        from_="+18329814427"
    )
except twilio.TwilioRestException as e:
    print e
from twilio.rest import TwilioRestClient

# To find these visit https://www.twilio.com/user/account
ACCOUNT_SID = "AC29506d85676c3f0ed4fc9131a7628b77"
AUTH_TOKEN = "91b3531c26ea646706ae5e37966e2e46"

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

message = client.messages.create(
    body="Hello Monkey!",  # Message body, if any
    to="+447807154765",
    from_="+442033897427",
)
print message.sid
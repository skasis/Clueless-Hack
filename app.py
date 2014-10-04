from flask import Flask, request
import simplejson
import os
import sendgrid
from twilio.rest import TwilioRestClient
import re
import datetime
import time

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    sg = sendgrid.SendGridClient('teamclueless', 'whatever214')

    message = sendgrid.Mail()
    message.add_to('John Doe <alexhygate@googlemail.com>')
    message.set_subject('Test Email')
    message.set_html('Body')
    message.set_text('Body')
    message.set_from('Doe John <doe@email.com>')
    sg.send(message)
    return "hi :)"
    
@app.route('/textmail',methods=['POST','GET'])
def text_mail():
    sg = sendgrid.SendGridClient('teamclueless', 'whatever214')
    message = sendgrid.Mail()
    day1 = datetime.date.today()
    
    ACCOUNT_SID = "AC29506d85676c3f0ed4fc9131a7628b77"
    AUTH_TOKEN = "91b3531c26ea646706ae5e37966e2e46"
    
    time.sleep(10)    
    
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    recent = client.messages.list(to="+442033897427",
        date_sent=day1)
    
    msg = recent[0].body
    
    to_address = re.search(r'[\w\.-]+@[\w\.-]+', msg)
    message.add_to(to_address.group(0))
    message.set_subject('Email via Text')
    message.set_html(msg)
    message.set_text(msg)
    message.set_from('Doe John <doe@email.com>')
    sg.send(message)
    return "hi :)"
    

@app.route('/parse', methods=['POST'])
def sendgrid_parser():    
    # Consume the entire email
    envelope = simplejson.loads(request.form.get('envelope'))
    
    # Get some header information
    to_address = envelope['to'][0]
    from_address = envelope['from']
    
    # Now, onto the body
    text = request.form.get('text')
    html = request.form.get('html')
    subject = request.form.get('subject')
    
    sg = sendgrid.SendGridClient('teamclueless', 'whatever214')
    
    # To find these visit https://www.twilio.com/user/account
    ACCOUNT_SID = "AC29506d85676c3f0ed4fc9131a7628b77"
    AUTH_TOKEN = "91b3531c26ea646706ae5e37966e2e46"
    
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    
    message = client.messages.create(
        body=text,  # Message body, if any
        to=subject,
        from_="+442033897427",
    )
    print message.sid

    message = sendgrid.Mail()
    message.add_to('John Doe <alexhygate@googlemail.com>')
    message.set_subject(subject)
    message.set_html('You have sent a text to '+ subject)
    message.set_text('You have sent a text to '+ subject)
    message.set_from('Doe John <doe@email.com>')
    sg.send(message)
    return "OK"
    



  
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
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
 
def strip_email(text, email):
    if not text.startswith(email):
        return text
    else:
        return text[len(email):]
   
@app.route('/textmail',methods=['POST','GET'])
def text_mail():
    sg = sendgrid.SendGridClient('teamclueless', 'whatever214')
    message = sendgrid.Mail()
    day1 = datetime.date.today()
    
    ACCOUNT_SID = "AC29506d85676c3f0ed4fc9131a7628b77"
    AUTH_TOKEN = "91b3531c26ea646706ae5e37966e2e46"
    
    time.sleep(15)    
    
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    recent = client.messages.list(to="+442033897427",
        date_sent=day1)
    
    msg = recent[0].body
    to_address = re.search(r'[\w\.-]+@[\w\.-]+', msg)
    msg_body = strip_email(msg,to_address.group(0))
    message.add_to(to_address.group(0))
    if msg_body == ' cats':
        message.set_subject('Cat via Text')
        message.set_html('<html><body><img src="http://placekitten.com/g/300/200" width="300" height="200" border="0" alt="cat"></body></html>')
    elif msg_body == ' fresh':
        message.set_subject('Fresh via Text')
        message.set_html('<html><body>In west Philadelphia born and raised<br>On the playground was where I spent most of my days<br>Chillin out maxin relaxin all cool<br>And all shootin some b-ball outside of the school<br>When a couple of guys who were up to no good<br>Started making trouble in my neighborhood<br>I got in one little fight and my mom got scared<br>She said Youre movin with your auntie and uncle in Bel Air</body></html>')
    elif msg_body == ' shrek':
        message.set_subject('Shrek via Text')
        message.set_html('<html><body><img src="http://rack.0.mshcdn.com/media/ZgkyMDE0LzA2LzE2LzIwL3NocmVrLmRyZWFtLmZkNGQ1LnBuZwpwCXRodW1iCTEyMDB4NjI3IwplCWpwZw/acf2ed18/328/shrek.dreamworks.tv_.jpg" width="400" height="209" border="0" alt="shrek"></body></html>')
    else:
        message.set_subject('Email via Text')
        message.set_html(msg_body)
        message.set_text(msg_body)
    message.set_from('Sophie Jones <s.a.jones72@gmail.com>')
    
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
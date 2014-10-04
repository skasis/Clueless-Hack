from flask import Flask, request
import simplejson
import sendgrid
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

    message = sendgrid.Mail()
    message.add_to('John Doe <alexhygate@googlemail.com>')
    message.set_subject(subject)
    message.set_html('Body')
    message.set_text('Body')
    message.set_from('Doe John <doe@email.com>')
    sg.send(message)
    return "OK"
  
if __name__ == "__main__":
    app.run(port=8080)
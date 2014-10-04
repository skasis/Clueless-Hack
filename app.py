from flask import Flask
import simplejson
app = Flask(__name__)

@app.route('/parse', methods=('POST'))
def sendgrid_parser(request):

      # Consume the entire email
      envelope = simplejson.loads(request.form.get('envelope'))
    
      # Get some header information
      to_address = envelope['to'][0]
      from_address = envelope['from']
    
      # Now, onto the body
      text = request.form.get('text')
      html = request.form.get('html')
      subject = request.form.get('subject')
    
      
      print(subject)
    
      return "OK"
  
if __name__ == "__main__":
  app.run()
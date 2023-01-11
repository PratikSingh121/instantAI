from flask import Flask, request
import os
import requests
import math
import openai
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TOKEN = 4000
PREMIUM_TOKEN = 10000

openai.api_key = "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"

app = Flask(__name__)

#############################################################################
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)

class database(db.Model):
    cno = db.Column(db.Integer, primary_key = True)
    token = db.Column(db.Integer, nullable = False)
    premium = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f'{self.cno}'

@app.route('/')
def index():
    return "404 Not Found"

def api_process(data):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=data,
    temperature=0.9,
    max_tokens=500,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6
    # stop=[" Human:", " AI:"]
    )

    resp = response.choices[0].text
    print(resp)
    return resp
 
def send_msg(msg, phone_no):
    headers = {
        'Authorization': 'Bearer EABU18QMaBQ4BANU01hY9EvBfKZBZBrK9VE49He7FK1Kr4u94JdQg6XRbIraYANS6ZC7DZCjsJ7pCZCaIEuZBIjDgbbF8onxeNmnxeV0fkc8ZBOGmbZBkUApZB9L6UlSI2jPeDMizMHg7NGgFJP2QYTWyrTe1H47erlSEk7WGRLIkYDdGPiRgcjgqeu4BEyDddFzcOOaKupxMTJQ6Dtd0ZAs7HZB'
        # 'Accept-Language' : 'en-US,en;q=0.5'
        # user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
   }
    json_data = {
        'messaging_product': 'whatsapp',
        'to': str(phone_no),
        'type': 'text',
        "text": {
            "body": msg
        }
    }
    response = requests.post('https://graph.facebook.com/v13.0/106970675621311/messages', headers=headers, json=json_data)
    print(response.text)

def create_data(phone_no):
    new = database(cno = phone_no, token = DEFAULT_TOKEN, premium = 0)
    db.session.add(new)
    db.session.commit()

@app.route('/receive_msg', methods=['POST','GET'])
def webhook():
    print(request)
    res = request.get_json()
    print(res)

    try:
        if res['entry'][0]['changes'][0]['value']['messages'][0]['id']:
            phone_no = int(res['entry'][0]['changes'][0]['value']['messages'][0]['from'])
            prompt = res['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            prompt_words = prompt.count(' ')+1
            if phone_no not in [data.cno for data in database.query.all()]:
                create_data(phone_no)
            pointer = db.session.query(database).filter_by(cno = phone_no).first()
            if prompt_words*2 < pointer.token:
                data = api_process(prompt)
                pointer.token =pointer.token - (data.count(' ')+prompt_words+1)
                db.session.add(pointer)
                db.session.commit()
                send_msg(data, phone_no)
            else:
                send_msg('Daily Limit Exceeded', phone_no)
                
    except:
        pass
    return '200 OK HTTPS.'
 
  
if __name__ == "__main__":
    app.run(debug=True)
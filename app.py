from flask import Flask, request
import requests
import math
import openai

openai.api_key = "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"

app = Flask(__name__)
 
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

# def process(data):
#     if len(data)>4096:
#         count = math.ceil(len(data)/4096)
#         arr = []
#         for i in range(count):
#             if len(data)<((i+1)*4096):
#                 end = len(data)
#                 print(f"end : {end}")
#             else:
#                 end = (i+1)*4096
#             start = i*4096
#             arr.append(data[start:end])
#         return arr
 
def send_msg(msg, phone_no):
    headers = {
        'Authorization': 'Bearer EABU18QMaBQ4BAG0ETRrw3OwedWow3IOGLxT22KyPZBVBVMER77ZCusybFQ2lERrB5a2yWFXN4aZCT6bc6zH1IZAobylzb2f29t4U40aeZCxYdeAM9wDZBogZAx95VL9Et44G438ojPE0913lXG9SpeZBg5tHp7v4YsEoNxnS0DO0QI73G5IqlZCveUVHfEeMmmE4IhJv0xZBwcy9aE97ZBuZCZBmB'
        # 'Accept-Language' : 'en-US,en;q=0.5'
        # user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
   }
    json_data = {
        'messaging_product': 'whatsapp',
        'to': phone_no,
        'type': 'text',
        "text": {
            "body": msg
        }
    }
    response = requests.post('https://graph.facebook.com/v13.0/106970675621311/messages', headers=headers, json=json_data)
    print(response.text)

@app.route('/receive_msg', methods=['POST','GET'])
def webhook():
    print(request)
    res = request.get_json()
    print(res)

    try:
        if res['entry'][0]['changes'][0]['value']['messages'][0]['id']:
            phone_no = res['entry'][0]['changes'][0]['value']['messages'][0]['from']
            data = api_process(res['entry'][0]['changes'][0]['value']['messages'][0]['text']['body'])
            # data = process(data)
            # for i in data:
            #    send_msg(i ,phone_no)
            send_msg(data, phone_no)
                
    except:
        pass
    return '200 OK HTTPS.'
 
  
if __name__ == "__main__":
    app.run(debug=True)

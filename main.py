from flask import Flask,request, render_template,jsonify
from twilio.twiml.messaging_response import MessagingResponse
import psycopg2
import requests
from twilio.rest import Client
import http.client, urllib, base64

app = Flask(__name__)
# @app.route("/")
# def home():
#     return ('Home page')

@app.route("/dashboard")
def dashboard():
    print('sree')
    return render_template('dashboard.html')

@app.route("/send-sms", methods = ['POST'])
def sendsms():
    account_sid= "AC9f9d5bd80de7123c6f6ec22634f08dc7"
    auth_token= "4d0e1bacf93d53098752af5bfe9949e9"
    client= Client(account_sid,auth_token)
    message = client.messages.create(
        body=request.form['message'],
        from_='+16506704698',
        to=request.form['phoneNumber']
    )
    print(message.sid)
    return message.sid

def execute_query(req):
    db = psycopg2.connect(host='127.0.0.1', port=5432,user='coke',password='coke')
    cur = db.cursor()
    query=req
    cur.execute(query)
    results= cur.fetchall()
    print(results)
    db.commit()
    cur.close()
    db.close()
    return (results)


@app.route("/")
def products():
    query = "Select product_name from product"
    result = execute_query(query)
    print(result)
    return render_template('dashboard.html', result=result)

def calculateSentimentAnalysis (body):
    documents = {'documents' : [
        {'id': '1', 'language': 'en', 'text': body}
    ]}
    url = 'https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment'
    headers   = {"Ocp-Apim-Subscription-Key": "5cb160e123e740ce9bf93b498f9fc670"}
    response  = requests.post(url, headers=headers, json=documents)
    sentiments = response.json()
    return sentiments['documents'][0]['score']  

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    print(request.form)
    body = request.form['Body']
    print(body)
    score = calculateSentimentAnalysis(body)
        
    resp = MessagingResponse()
    if (score >= 0.5):
        resp.message("Great.Can you describe what you love most about product?")
    else:
        resp.message("I'm Sorry to hear that. what do you dislike about product?")
        
    return str(resp)

if __name__ == "__main__":
    
    print("Start program")
    db = psycopg2.connect(host='127.0.0.1', port=5432,user='coke',password='coke')
    cur = db.cursor()
    query = "Select * from coke.company"
    # cur.execute("use coke")
    cur.execute(query)
    results= cur.fetchall()
    print(results)
    db.commit()
    cur.close()
    db.close()
    print('db success')

    app.run(debug=True)
    


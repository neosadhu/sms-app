from flask import Flask, redirect, url_for, request
from MailClient import MailJetClient
import os
import time
import util
import requests

api_key = os.environ['MJ_APIKEY_PUBLIC']
api_secret = os.environ['MJ_APIKEY_PRIVATE']
mail_client = MailJetClient(api_key,api_secret)
app = Flask(__name__)
db_client = util.connect_to_db()



@app.route('/messages',methods = ['POST','GET'])
def messages():
    
    if request.method == 'POST':
        # Get POST data as json & read it as a DataFrame
        req_body = request.get_json()

        try:
        #SEND THE SMS
            res=mail_client.send_mail(sender=req_body['email'],receivers=req_body['receivers'],subject=req_body['subject'],payload=req_body['body'])
        except Exception as e:
            print (requests.RequestException)
        
        if res.status_code == 200:
            message_id = str(res.json()['Sent'][0]['MessageID'])
            message_content = request.get_json()['body']
        #ADD TO DB; 
            util.add_message(dbClient=db_client,message_id=message_id,message=message_content)
        
        return ({"status_code":res.status_code, "response_details":res.json()['Sent'][0]})
    
    elif request.method == 'GET':
        results = db_client.execute_query(util.select_messages_query)
        print (results)
        print(results[0])
        return ([{"id":str(result[1]), "message_content":str(result[2]), "time":str(result[3])} for result in results])

@app.route('/message/<id>',methods = ['GET'])
def get_message(id:str):
    result = util.get_message(dbClient=db_client,message_id=id)
    return ({"id":str(result[1]),"message_content":str(result[2]), "time":str(result[3])})

if __name__ == "__main__":
    app.run()
    
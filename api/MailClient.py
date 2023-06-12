import requests
import typing
import time


from mailjet_rest import Client


class MailJetClient ():
    
    def __init__(self, mj_public_key:str, mj_private_key:str):
        self.mj_private_key = mj_private_key
        self.mj_public_key = mj_public_key
        self.mailjet = Client(auth=(mj_public_key, mj_private_key))

    def send_mail(self,sender:str, receivers:list, subject:str, payload:str) -> requests.Response:
        receipientsList=[]
        for r in receivers:
            receipientsList.append({'Email':r})            
        data = {
	            'FromEmail': sender,
	            # 'FromName': 'Bhoot!!!!',
	            'Subject': subject,
	            'Text-part': payload,
	            'Recipients': receipientsList
                }
        result = self.mailjet.send.create(data=data) 
        return result       





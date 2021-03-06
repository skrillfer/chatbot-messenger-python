# encoding: utf-8
import webapp2
import json
import logging
from google.appengine.api import urlfetch
from bot import Bot
import yaml
from user_events import UserEventsDao
VERIFY_TOKEN = 'token_skr!llf3r'
ACCESS_TOKEN = 'EAACvuQz92A0BAJ6a01NCirZAleaQiLxjeNZBEA3Mc8MMOKRffYZBVquutrseV2PIZA8og5e9XRGtIZAyiOBqu2ZBJpDbSKzZC8BBKb7yly7xPQfTyvDebsfZA4sel5cc75ZCsqUuz2sGQECASZApAv1GiJlCZAUFa6jqxcUSvETaJGybQZDZD'

class MainPage(webapp2.RequestHandler):
    def __init__(self,request = None, response = None):
        super(MainPage,self).__init__(request,response)
        logging.info('Instanciando bot')
        tree = yaml.load(open('tree.yaml'))
        dao =UserEventsDao()
        self.bot = Bot(send_message,dao,tree)
        #dao.add_user_event('123','Luis Ramirez', 'abc')
        #data=dao.get_user_events('123')
        #print data
        #dao.remove_user_events('123')

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        mode = self.request.get('hub.mode')
        if mode == 'subscribe':
            challenge = self.request.get('hub.challenge')
            verify_token = self.request.get('hub.verify_token')
            if verify_token == VERIFY_TOKEN:
                self.response.write(challenge)
        else:
            self.response.write('Ok')
    
    def post(self):
        data = json.loads(self.request.body)
        logging.info('Data obtenida desde messenger: %r',data)
        if data['object'] == 'page':
            for entry in data['entry']:
                for messagin_event in entry['messaging']:
                    sender_id = messagin_event['sender']['id']
                    recipient_id = messagin_event['recipient']['id']
                    if messagin_event.get('message'):
                        is_admin = False
                        message = messagin_event['message']
                        if message.get('is_echo'):
                            if message.get('app_id'): #bot
                                # ignore echo message
                                continue
                            else: # admin
                                #disable bot
                                is_admin = True
                        message_text = messagin_event['message'].get('text','')
                        logging.info('Mensaje: %s',message_text)
                        #bot handle
                        if is_admin:
                            sender_id = recipient_id
                        self.bot.handle(sender_id,message_text,is_admin)
                    if messagin_event.get('postback'):
                        message_text = messagin_event['postback']['payload']
                        #bot handle
                        self.bot.handle(sender_id,message_text)
                        logging.info('Post-back: %s',message_text)
    
def send_message(recipient_id,message_text,possible_answers):
    logging.info("Enviando mensaje a  %r: %s", recipient_id,message_text)
    headers = {
        'Content-Type': 'application/json'
    }
    #message = {'text': message_text}
    #max buttons quantity : 3
    #max placeholder button  length : 20 characters
    message = get_postback_buttons_message(message_text,possible_answers)
    if message is None:
        message ={'text':message_text}
    raw_data = {
        'recipient':{
            'id': recipient_id
        },
        'message': message
    }
    data = json.dumps(raw_data)
    r = urlfetch.fetch('https://graph.facebook.com/v2.6/me/messages?access_token=%s' % ACCESS_TOKEN,
        method= urlfetch.POST, headers=headers, payload = data
    )
    if r.status_code != 200:
        logging.error("Error %r enviando mensaje: %s", r.status_code,r.content)

def get_postback_buttons_message(message_text,possible_answers):
    if len(possible_answers) == 0 or len(possible_answers) > 3:
        return None
    buttons = []
    for answer in possible_answers:
        buttons.append({
            'type' : 'postback',
            'title' : answer,
            'payload' : answer
        })
    return {
        'attachment': {
            'type': 'template',
            'payload': {
                'template_type': 'button',
                'text': message_text,
                'buttons': buttons
            }
        }
    }

class PrivacyPolicyPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        htmlContent = open('privacy-policy.html').read()
        self.response.write(htmlContent)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/privacy-policy', PrivacyPolicyPage),
], debug=True)
#text
#https://developers.facebook.com/docs/messenger-platform/webhook/
#https://developers.facebook.com/docs/messenger-platform/reference/buttons/postback
#yet another markup language: yaml
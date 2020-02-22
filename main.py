# encoding: utf-8
import webapp2
import json
import logging
from google.appengine.api import urlfetch

VERIFY_TOKEN = 'token_skr!llf3r'
ACCESS_TOKEN = 'EAACvuQz92A0BAJ6a01NCirZAleaQiLxjeNZBEA3Mc8MMOKRffYZBVquutrseV2PIZA8og5e9XRGtIZAyiOBqu2ZBJpDbSKzZC8BBKb7yly7xPQfTyvDebsfZA4sel5cc75ZCsqUuz2sGQECASZApAv1GiJlCZAUFa6jqxcUSvETaJGybQZDZD'

class MainPage(webapp2.RequestHandler):
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
                    if messagin_event.get('message'):
                        message = messagin_event['message']
                        message_text = messagin_event['message'].get('text','')
                        logging.info('Mensaje: %s',message_text)
                        send_message(sender_id,'Hola, soy un bot')
                    if messagin_event.get('postback'):
                        logging.info('Post-back')
    
def send_message(recipient_id,message_text):
    logging.info("Enviando mensaje a  %r: %s", recipient_id,message_text)
    headers = {
        'Content-Type': 'application/json'
    }
    #message = {'text': message_text}
    possible_answers = ['Opcion A','Opcion B', 'Opcion C']
    message = get_postback_buttons_message(message_text,possible_answers)
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
        logging.error("Error enviando mensaje: %r", r.status_code)

def get_postback_buttons_message(message_text,possible_answers):
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

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
#text
#https://developers.facebook.com/docs/messenger-platform/webhook/
#https://developers.facebook.com/docs/messenger-platform/reference/buttons/postback
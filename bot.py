# -*- coding: utf-8 -*-
import logging

class Bot(object):
    def __init__(self, send_callback, users_dao, tree):
        self.send_callback = send_callback
        self.users_dao = users_dao#data access object
        self.tree = tree
    
    def handle(self,user_id,user_message):
        logging.info("Se invoco el metodo handle")
        #get history events and messages
        history = [
            (u'Hola! Por favor selecciona una opción para poder ayudarte.','bot'),
            (u'Cursos disponibles','user'),
            (u'Tenemos varios cursos! Todos ellos son muy interesantes y totalmente prácticos. Por favor selecciona la opción que te resulte más interesante.','bot'),
            (user_message,'user')
        ]
        message_text = self.tree['say']
        possible_answers = self.tree['answers'].keys()
        tree = self.tree
        for text, author in history:
            if author == 'bot':
                if text == tree['say']:
                    tree = tree['answers']
            elif author == 'user':
                key = get_key_if_valid(text, tree)
                if key is not None:
                    tree = tree[key]
                    if 'say' in tree:
                        message_text = tree['say']
                    if 'answers' in tree:
                        possible_answers =  tree['answers'].keys()
                    else:
                        possible_answers = None
        possible_answers.sort()
        self.send_callback(user_id,message_text,possible_answers)

def get_key_if_valid(text,dictionary):
    for key in dictionary:#alwas iterate dictionary in key.
        if key.lower() == text.lower():
            return key
    return None

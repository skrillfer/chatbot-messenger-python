# -*- coding: utf-8 -*-
import logging
DEFAULT_RESPONSE = 'Disculpa no entendí, deseas volver a empezar?'
DEFAULT_POSSIBLE_ANSWERS = ['Sí','No']

class Bot(object):
    def __init__(self, send_callback, users_dao, tree):
        self.send_callback = send_callback
        self.users_dao = users_dao#data access object
        self.tree = tree
    
    def handle(self,user_id,user_message):
        logging.info("Se invoco el metodo handle")
        #put the last message of user
        self.users_dao.add_user_event(user_id,'user',user_message)
        #get history events and messages
        history = self.users_dao.get_user_events(user_id)
        
        tree = self.tree
        new_conversation = True
        for text, author in history:
            if author == 'bot':
                new_conversation = False
                if 'say' in tree and text == tree['say'] and 'answers' in tree:
                    tree = tree['answers']
            elif author == 'user':
                if new_conversation:
                    response_text = tree['say']
                    possible_answers = tree['answers'].keys()
                    possible_answers.sort()
                else:
                    key = get_key_if_valid(text, tree)
                    if key is None:
                        response_text = DEFAULT_RESPONSE
                        possible_answers = DEFAULT_POSSIBLE_ANSWERS
                    else:
                        tree = tree[key]
                        if 'say' in tree:
                            response_text = tree['say']
                        if 'answers' in tree:
                            possible_answers =  tree['answers'].keys()
                        else:
                            possible_answers = []
        possible_answers.sort()
        self.send_callback(user_id,response_text,possible_answers)
        self.users_dao.add_user_event(user_id,'bot',response_text)

def get_key_if_valid(text,dictionary):
    for key in dictionary:#alwas iterate dictionary in key.
        if key.lower() == text.lower():
            return key
    return None

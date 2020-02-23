# -*- coding: utf-8 -*-
import logging

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
        response_text = self.tree['say']
        possible_answers = self.tree['answers'].keys()
        possible_answers.sort()
        tree = self.tree
        for text, author in history:
            if author == 'bot':
                if 'say' in tree and text == tree['say']:
                    tree = tree['answers']
            elif author == 'user':
                key = get_key_if_valid(text, tree)
                if key is not None:
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

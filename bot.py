import logging

class Bot(object):
    def __init__(self, send_callback, users_dao, tree):
        self.send_callback = send_callback
        self.users_dao = users_dao#data access object
        self.tree = tree
    
    def handle(self,user_id,user_message):
        logging.info("Se invoco el metodo handle")
        #get history events and messages
        message_text = self.tree['say']
        possible_answers = self.tree['answers'].keys()
        possible_answers.sort()
        self.send_callback(user_id,message_text,possible_answers)
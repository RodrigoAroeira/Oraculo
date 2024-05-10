import time 
time.clock = time.time

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

rapaizinho = ChatBot('Rapazinho', 
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
         {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Desculpa, ainda estou aprendendo!',
            'maximum_similarity_threshold': 0.80,
        }],
    
    database_uri='sqlite:///database.sqlite3')

trainer = ChatterBotCorpusTrainer(rapaizinho)

# Train the chatbot based on the portuguese corpus
trainer.train("chatterbot.corpus.portuguese")
trainer.train("chatterbot.corpus.portuguese.conversations")

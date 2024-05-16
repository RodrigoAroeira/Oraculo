from collections import defaultdict
import string
import random

class Markov():
    def __init__(self, file_path):
        self.file_path = file_path
    
        self.text = self.get_text().translate(str.maketrans('','', string.punctuation))
        self.model = self.model()
        
    def get_text(self):
        text = []
        for line in open(self.file_path):
            text.append(line)
        return ' '.join(text)
    
    def model(self):
        words = self.text.split(' ')
        markov_dict = defaultdict(list)
    
        for current_word, next_word in zip(words[0:-1], words[1:]):
            markov_dict[current_word].append(next_word)

        markov_dict = dict(markov_dict)
        # print('Treinado com sucesso!')
        return markov_dict
      
def predict_words(chain, first_word, number_of_words=5):
    if first_word in list(chain.keys()):
        word1 = str(first_word)
        
        predictions = word1.capitalize()

        for i in range(number_of_words-1):
            word2 = random.choice(chain[word1])
            word1 = word2
            predictions += ' ' + word2
        return predictions
    else:
        return "Palavra não foi treinada."
  
if __name__ == '__main__':
    m = Markov(file_path='data/prompts.txt')
    chain = m.model
    print(predict_words(chain, first_word = 'eu', number_of_words = 5))
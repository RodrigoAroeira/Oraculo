from collections import defaultdict
import random

class Markov:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_lines(self) -> list[str]:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.

    @property
    def model(self) -> dict[str, list[str]]:
        lines = self.get_lines()
        markov_dict = defaultdict(list)

        for line in lines:
            word = line.strip().split()
            for current_word, next_word in zip(words[:-1], words[1:]):
                if current_word and next_word:
                    markov_dict[current_word].append(next_word)

        return dict(markov_dict)

def predict_words(chain: dict, first_word: str, number_of_words: int=5):
    if first_word in list(chain.keys()):
        word1 = str(first_word)

        predictions = word1.capitalize()

        for i in range(number_of_words-1):
            if len(chain[word1]) == 0:
                break
            word2 = random.choice(chain[word1])
            word1 = word2
            predictions += ' ' + word2

        punctuations = ['!', '.', '?']
        wrong_finishing = [',', ';', ':']
        temp = list(predictions)
        if temp[-1] in wrong_finishing:
            temp.pop(-1)
            temp.append(random.choice(punctuations))

        elif temp[-1] not in punctuations:
            temp.append('.')

        # print(temp)

        final_prediction = ''.join([str(item) for item in temp])

        return final_prediction
    else:
        return "Palavra não foi treinada."
  
if __name__ == '__main__':
    m = Markov(file_path='data/prompts.txt')
    chain = m.model
    print(predict_words(chain, first_word = 'eu', number_of_words = 5))

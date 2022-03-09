import csv

class NGdetector:
    __NG_words = []
    def __init__(self, threshold=-0.5):
        with open('./NGwords.csv', 'r', encoding='utf-8') as f:
            for w in f.readlines():
                self.__NG_words.append(w.rstrip('\n'))

    def check(self, text: str) -> bool:
        for w in self.__NG_words:
            if w in text:
                return False
        return True

import os


class NGdetector:
    __NG_words = []

    def __init__(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        with open(f"{dir}/NGwords.csv", 'r', encoding='utf-8') as f:
            for w in f.readlines():
                self.__NG_words.append(w.rstrip('\n'))

    def check(self, text: str) -> bool:
        for w in self.__NG_words:
            if w in text:
                return False
        return True

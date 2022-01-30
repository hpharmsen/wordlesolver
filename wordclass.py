import json
import random


class Words:
    def __init__(self, lang):
        with open(lang + '/letters.json') as f:
            self.frequencies = json.load(f)
        with open(lang + '/words.txt') as f:
            self.words = [w.strip() for w in f.readlines()]
        self._index = -1

    def match(self, pattern):
        return [word for word in self.words if all([p in (w, '?') for w, p in zip(word, pattern )])]

    def sort_on_letter_frequency(self):
        def tot_freq(word):
            return sum([self.frequencies[l] for l in list(set(word))])
        self.words.sort(key=tot_freq, reverse=True)
        return self

    def extended_match(self, pattern:str, unused_letters:set, wrongly_placed_letters:list[str]):

        def check_for_wrongly_placed_letters():
            for i, w in enumerate(wrongly_placed_letters):
                for letter in w:
                    if word[i]==letter:
                        return False # wrongly placed
                    if not word.count(letter):
                        return False # letter not in word at all
            return True

        result = []
        for word in self.words:
            if not check_for_wrongly_placed_letters():
                continue

            if all([p in (w,'?') and not w in unused_letters for w,p in zip( word, pattern )]):
                result += [word]
        return result

    def anagram(self, word:str):
        word_set = set(word)
        return [w for w in self.words if set(w)==word_set and w != word]

    def choice(self):
        return random.choice(self.words)

    def __getitem__(self, key):
        return self.words[key]

    def __len__(self):
        return len(self.words)

    def __iter__(self):
        return self

    def __next__(self):
        self._index += 1
        if self._index < len(self.words):
            return self.words[self._index]
        self._index = -1
        raise StopIteration


if __name__=='__main__':
    words = Words('nl')
    #matches =  words.match('bol??')
    #print(matches)
    anagrams = words.anagram('stoel')
    print(anagrams)
    for w in words[:13]:
        print( w )

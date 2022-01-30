#import random
from collections import Counter

from wordclass import Words

def check( word, guess):
    pattern = ''
    wrongplace = ['','','','','']
    unused = set()
    for i in range(len(word)):
        if guess[i] == word[i]:
            pattern += word[i]
        else:
            if word.count(guess[i]):
                wrongplace[i] = wrongplace[i]+guess[i]
            else:
                unused.add(guess[i])
            pattern += '?'
    return pattern, wrongplace, unused


def guess_word(guess_count:int, words:Words, full_pattern:str, unused_letters:set, wrongly_placed_letters:list[str]):

    matches = words.extended_match(full_pattern, unused_letters, wrongly_placed_letters)
    if len(matches)+guess_count<=6:
        guess = matches[0]
        matches = matches[1:]
    else:
        letters_with_info = unused_letters.union(full_pattern).union(''.join(wrongly_placed_letters))
        c = Counter(''.join(matches))
        score = lambda word: sum(0 if l in letters_with_info else c[l] for l in set(word))

        scored = {word:score(word) for word in words}
        guess = sorted(words, key=lambda w:scored[w], reverse=True)[0]
        try:
            matches.remove(guess)
        except ValueError:
            pass
    words.words = matches
    return guess

def merge_pattern( full_pattern, pattern ):
    res = [pattern[i] if full_pattern[i]=='?' else full_pattern[i] for i in range(len(pattern))]
    return ''.join(res)

def merge_wrongly_placed(wrongly_placed_letters, wrongplace):
    for i, w in enumerate(wrongplace):
        for letter in w:
            if not wrongly_placed_letters[i].count(letter):
                wrongly_placed_letters[i] += letter
    return wrongly_placed_letters

def play_game(words:Words, guess_func, word=None, output=True, verbose=False):
    if not word:
        word = words.choice()
    full_pattern = '?????'
    unused_letters = set()
    wrongly_placed_letters = ['','','','','']
    guess = guess_func(0, words, full_pattern, unused_letters, wrongly_placed_letters)
    guess_count = 1
    if verbose:
        print()
    guesses = [guess]
    while guess != word:
        pattern, wrongplace, unused = check(word, guess)
        unused_letters.update(unused)
        wrongly_placed_letters = merge_wrongly_placed(wrongly_placed_letters, wrongplace)
        full_pattern = merge_pattern(full_pattern, pattern)
        if verbose:
            print( guess, full_pattern, wrongly_placed_letters, ''.join(unused_letters) )
        elif output:
            print(guess)
        guess =  guess_func(guess_count, words, full_pattern, unused_letters, wrongly_placed_letters)
        guesses += [guess]
        guess_count +=1
    if output:
        print( guess, '!' )
    if guess_count>6:
        print( guesses )
    return guess_count


def streak(lang, guess_func, number=1000):
    win = 0
    loose = 0
    words = Words(lang).sort_on_letter_frequency()
    full_list = words[:]
    while win+loose < number:
        words.words = full_list[:]
        if play_game(words, guess_func, output=False, verbose=False) <= 6:
            win+=1
        else:
            loose +=1
            print(win, loose)
    print( win, loose )

def full_streak(lang, guess_func):
    win = 0
    loose = 0
    words = Words(lang).sort_on_letter_frequency()
    full_list = words.words[:]
    for word in full_list:
        words.words = full_list[:]
        if play_game(words, guess_func, word=word, output=False, verbose=False) <= 6:
            win+=1
        else:
            loose +=1
            print(win, loose)
    print( win, loose )
    print( round(100*win/(win+loose),1))


if __name__=='__main__':
    #play_game(Words('wordle').sort_on_letter_frequency(), guess_word, 'hover')
    full_streak('wordle', guess_word)
    #full_streak('nl', guess_word)
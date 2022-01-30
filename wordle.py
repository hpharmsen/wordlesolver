import sys

from game import play_game, guess_word
from wordclass import Words

if __name__=='__main__':
    words = Words('wordle').sort_on_letter_frequency()
    word = sys.argv[1] if sys.argv[1:] else words.choice()
    play_game(words, guess_word, word)
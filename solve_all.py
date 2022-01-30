from game import play_game, guess_word
from wordclass import Words


def full_streak(lang, guess_func):
    win = 0
    loose = 0
    words = Words(lang).sort_on_letter_frequency()
    full_list = words.words[:]
    for word in full_list:
        words.words = full_list[:]
        if play_game(words, guess_func, word=word, output=False, verbose=False) <= 6:
            win += 1
        else:
            loose += 1
            print(win, 'wins,', loose, 'losses')
    print(win, loose)
    print(round(100 * win / (win + loose), 1))


if __name__ == "__main__":
    full_streak("wordle", guess_word)

# import random
from collections import Counter

from wordclass import Words


def check(word: str, guess: str):
    """Checks the given guess agains the guessable word
        returns a (pattern, wrongplace, unused) tuple where
        pattern is in the form '??es?' showing the right letters
        wrongplace is a list of 5 strings, one for each position, containing the letters
          that are right but not for that position. e.g. ['ah','','a','','']
        unused is a set containing letters that we now now, do not appear in the word.
    """
    pattern = ""
    wrongplace = ["", "", "", "", ""]
    unused = set()
    for i in range(len(word)):
        if guess[i] == word[i]:
            pattern += word[i]
        else:
            if word.count(guess[i]):
                wrongplace[i] = wrongplace[i] + guess[i]
            else:
                unused.add(guess[i])
            pattern += "?"
    return pattern, wrongplace, unused


def merge_pattern(full_pattern, pattern):
    res = [
        pattern[i] if full_pattern[i] == "?" else full_pattern[i]
        for i in range(len(pattern))
    ]
    return "".join(res)


def merge_wrongly_placed(wrongly_placed_letters, wrongplace):
    for i, w in enumerate(wrongplace):
        for letter in w:
            if not wrongly_placed_letters[i].count(letter):
                wrongly_placed_letters[i] += letter
    return wrongly_placed_letters


def play_game(words: Words, guess_func, word=None, output=True, verbose=False):
    if not word:
        word = words.choice()
    full_pattern = "?????"
    unused_letters = set()
    wrongly_placed_letters = ["", "", "", "", ""]
    guess = guess_func(0, words, full_pattern, unused_letters, wrongly_placed_letters)
    guess_count = 1
    if verbose:
        print()
    guesses = [guess]
    while guess != word:
        pattern, wrongplace, unused = check(word, guess)
        unused_letters.update(unused)
        wrongly_placed_letters = merge_wrongly_placed(
            wrongly_placed_letters, wrongplace
        )
        full_pattern = merge_pattern(full_pattern, pattern)
        if verbose:
            print(guess, full_pattern, wrongly_placed_letters, "".join(unused_letters))
        elif output:
            print(guess)
        guess = guess_func(
            guess_count, words, full_pattern, unused_letters, wrongly_placed_letters
        )
        guesses += [guess]
        guess_count += 1
    if output:
        print(guess, "!")
    if guess_count > 6:
        print(guesses)
    return guess_count


def guess_word(
        guess_count: int,
        words: Words,
        full_pattern: str,
        unused_letters: set,
        wrongly_placed_letters: list[str],
):
    matches = words.extended_match(full_pattern, unused_letters, wrongly_placed_letters)
    if len(matches) + guess_count <= 6:
        guess = matches[0]
        matches = matches[1:]
    else:
        letters_with_info = unused_letters.union(full_pattern).union(
            "".join(wrongly_placed_letters)
        )
        c = Counter("".join(matches))
        score = lambda word: sum(
            0 if letter in letters_with_info else c[letter] for letter in set(word)
        )

        scored = {word: score(word) for word in words}
        guess = sorted(words, key=lambda w: scored[w], reverse=True)[0]
        try:
            matches.remove(guess)
        except ValueError:
            pass
    words.words = matches
    return guess

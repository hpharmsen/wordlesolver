# wordlesolver
Algorithm that tries to solve all wordle puzzles within 6 tries.

The project consists of a couple of parts.

### wordclass.py
General purpose class to do operations on lists of words.
It is initialized with a folder which should contain a words.txt word list and a letters.json file with letter frequencies in the language used. Like this:
```python
words = Words("wordle")
```
the Words class can do things like match words on a pattern or get anagrams.
```python
words.match('bl?ck')
words.anagram('clones')
```

### wordle.py
Without parameter, it chooses a random word and then tries to solve it.
```bash
python wordle.py
 
alert
disco
prune
serve !
```

With a parameter, it tries to solve the word given
```bash
python wordle.py
 
alert
noisy
stump
stock !
```

### woordle.py
Same as wordle.py but uses the dutch word list from the nl folder.

### game.py
Contains the logic to play a game (play_game), check a given guess (guess) and my best algorithm so far to come up with 
the best guess (guess_word).

### solve_all.py
The script that runs play_game on the full list of words with the given word guessing function.
My goal: that this script returns 100% wins. With the current guess_word function from game.py as the guess_func it 
reaches 99,6%.
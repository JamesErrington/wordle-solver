import re
import random
import statistics

chars = set('abcdefghijklmnopqrstuvwxyz')


def prune_word_list(word_list: list, template: str, included: set, not_included: set):
    regex_str = "^"
    for c in template:
        if c == "_":
            possibles = chars.difference(not_included)
            regex_str += f"[{''.join(possibles)}]"
        else:
            regex_str += f"[{c}]"
    regex_str += "$"

    matches = []
    for word in word_list:
        if re.match(regex_str, word):
            includes = all(map(lambda l: l in word, included))
            if len(included) == 0 or includes:
                matches.append(word)

    return matches


def calculate_letter_frequency(words: list):
    frequencies = dict()
    for letter in chars:
        n = 0
        for word in words:
            if letter in word:
                n += 1
        frequencies[letter] = n
    return frequencies


def pick_best_guess(words: list, frequencies: dict):
    scores = dict()
    for word in words:
        score = 0
        for letter, freq in frequencies.items():
            if letter in word:
                score += freq
        scores[word] = score
    best_score = max(scores.values())
    best_words = list(filter(lambda x: x[1] == best_score, scores.items()))

    return random.choice(best_words)[0]


def make_guess(answer: str, guess: str, included: set, not_included: set):
    template = ""
    for i, letter in enumerate(guess):
        if answer[i] == letter:
            template += letter
        elif letter in answer:
            template += "_"
            included.add(letter)
        else:
            template += "_"
            not_included.add(letter)
    return template


word_list = []
with open("words.txt") as file:
    word_list = file.read().splitlines()

RUNS = 1000
history = []
for _ in range(RUNS):
    answer = random.choice(word_list)
    guesses = 0

    matches = word_list
    template = "_____"
    included = set()
    not_included = set()

    while(True):
        guesses += 1
        matches = prune_word_list(matches, template, included, not_included)
        if(len(matches) == 0):
            print("No matching words found!")
            exit(1)

        frequencies = calculate_letter_frequency(matches)
        guess = pick_best_guess(matches, frequencies)
        template = make_guess(answer, guess, included, not_included)

        if(template == guess):
            history.append(guesses)
            break

print(f"Finished {RUNS} runs")
print(f"Mean guesses: {statistics.mean(history)}")
print(f"Median guesses: {statistics.median(history)}")
print(f"Max guesses: {max(history)}")
print(f"Min guesses: {min(history)}")

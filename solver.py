from statistics import mean, median
from timeit import default_timer
from typing import Dict, List, Set
from sortedcontainers import SortedList

chars = 'abcdefghijklmnopqrstuvwxyz'
CORRECT = "CORRECT"
PRESENT = "PRESENT"
ABSENT = "ABSENT"


def make_initial_template():
    return [set(chars), set(chars), set(chars), set(chars), set(chars)]


def prune_word_list(word_list: List[str], template: List[Set[str]]):
    matches = []
    for word in word_list:
        include = True
        for i, letter_set in enumerate(template):
            if word[i] not in letter_set:
                include = False
                break
        if include:
            matches.append(word)
    return matches


def calculate_letter_frequency(words: List[str], template: List[Set[str]]):
    letters = set([letter for present in template for letter in present])
    freqs = dict()
    for letter in letters:
        scores = []
        for i in range(5):
            score = 0
            for word in words:
                if word[i] == letter:
                    score += 1
            scores.append(score)

        freqs[letter] = scores
    return freqs


def pick_best_guess(words: List[str], freqs: Dict[str, int]):
    scores = SortedList()
    for word in words:
        score = 0
        for i, letter in enumerate(word):
            score -= freqs[letter][i]
        scores.add((score, word))
    # print(scores)
    return scores[0][1]


def make_guess(answer: str, guess: str, template: List[Set[str]]):
    results = []
    correct = 0
    for answer_letter, guess_letter in zip(answer, guess):
        if answer_letter == guess_letter:
            result = CORRECT
            correct += 1
        elif guess_letter in answer:
            result = PRESENT
        else:
            result = ABSENT
        results.append((guess_letter, result))
    if correct == len(template):
        return [], True

    for i, (letter, result) in enumerate(results):
        for j, letters in enumerate(template):
            if i == j and result == CORRECT:
                letters.clear()
                letters.add(letter)
            elif i == j and result == PRESENT:
                letters.discard(letter)
            elif result == ABSENT:
                letters.discard(letter)
    return template, False


with open("guesses.txt") as file:
    guess_words = file.read().splitlines()

with open("answers.txt") as file:
    answer_words = file.read().splitlines()

test_guesses = answer_words
num_guesses = len(test_guesses)
test_answers = answer_words
num_answers = len(test_answers)

history = []
incorrect = []
times = []
for i, answer in enumerate(test_answers):
    if i == num_answers // 4:
        print(f"25% ({i + 1} words)")
    elif i == num_answers // 2:
        print(f"50% ({i + 1} words)")
    if i == (3 * num_answers) // 4:
        print(f"75% ({i + 1} words)")

    start_time = default_timer()
    guess_pool = test_guesses
    template = make_initial_template()
    guesses = 0

    while True:
        guesses += 1
        guess_pool = prune_word_list(guess_pool, template)

        if len(guess_pool) == 0:
            print("No matching words found!")
            exit(1)

        freqs = calculate_letter_frequency(guess_pool, template)
        best_guess = pick_best_guess(guess_pool, freqs)
        template, correct = make_guess(answer, best_guess, template)

        if correct:
            history.append(guesses)
            if guesses > 6:
                incorrect.append((answer, guesses))
            times.append(default_timer() - start_time)
            break

print(f"Tested {num_answers} answers with {num_guesses} guesses")
print(f"Minimum guesses: {min(history)}")
print(f"Maximum guesses: {max(history)}")
print(f"Mean guesses: {mean(history)}")
print(f"Median guesses: {median(history)}")
print(f"> 6 guesses: {len(incorrect)}")
print(f"Minimum time: {min(times)}")
print(f"Maximum time: {max(times)}")
print(f"Mean time: {mean(times)}")
print(f"Median time: {median(times)}")
print(sorted(incorrect, key=lambda elem: elem[1]))

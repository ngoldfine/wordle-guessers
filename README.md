# Wordle Guessers
Comparison of algorithms for solving Wordle puzzles

Requirements: Python 3.8

Wordle is an online word game where players attempt to correctly guess a five-letter word. After each guess, the puzzle gives color-coded feedback for each letter in the word the player guessed. If a letter turns green, it is in the correct place within the word. If a letter is gold or yellow, that letter is in the solution but not in the right spot in the guess. If a letter is gray, that means the letter is not in the solution at all. If the correct word is guessed within six turns, the player wins the game. A new Wordle puzzle is available every day.

The WordleGuessers project tests out different algorithms for solving Wordle puzzles. I made this project in 2022. I implemented and tested three different algorithms (plus a baseline that guesses words at random). I used a list of all Wordle solutions and a list of all accepted Wordle guesses as vocabularies of possible guesses.

## Algorithms

Each algorithm is implemented as a subclass of the WordleGuesser class. WordleGuesser and its subclasses are in the game folder, in the files wordle_guesser.py, entropy_guesser.py, similarity_guesser.py and min_vocab_guesser.py.

### WordleGuesser

Randomly selects a word from the set of possible guesses.

WordleGuesser is the superclass of the other guesser classes, and is used as a random baseline for testing the effectiveness of the other guessers.

### EntropyGuesser

Selects the guess that maximizes entropy over all possible color feedback from the Wordle game (e.g. gray-green-yellow-yellow-green).

In information theory, entropy is a measure of uncertainty. Maximizing this uncertainty over the 243 possible permutations of gray, yellow and green in the color feedback results in guessing a word that makes each feedback option as close as possible to equally likely. The idea to use entropy to solve Wordle puzzles comes from [3Blue1Brown on Youtube](https://www.youtube.com/watch?v=v68zYyaEmEA). 

### SimilarityGuesser

Selects the guess that is most orthographically similar to the set of remaining guesses as a whole. Here similarity is defined based on the minimum edit distance between two words.

The reasoning behind this strategy is that knowing a particular letter is in a solution word narrows down the possible solutions more than knowing that a letter is not in the solution. By choosing the guess that is the most orthographically “typical” of the set of possible guesses, the chances of guessing letters that are in the correct spot within a solution (or in the solution at all) are high.

### MinVocabGuesser

Selects the guess that will, on average, remove the largest number of words from the set of possible guesses.

The fewer options there are for a guess, the more likely it is that the next guess will be correct. MinVocabGuesser’s strategy is to shrink the guess vocabulary as much as possible in as few guesses as possible.

## Vocabularies

The experiments use two vocabularies. Guessers can be set to use either vocabulary as their initial set of possible guesses. Both vocabularies were copied from the Wordle source code in January 2022.

### Small vocabulary

This is the set of all 2,315 past and future Wordle solutions.

### Large vocabulary

This is the set of all 12,972 words that Wordle accepts as a guess.

## Experiments

Three experiments were run to test the effectiveness of the entropy, similarity and minimum-vocabulary algorithms and compare them to a random baseline. The experiments involved using the algorithms to solve puzzles and calculating the average number of guesses required to finish a puzzle, and the win rate (the percent of puzzles solved within six guesses). The guessing time per puzzle was also calculated. 

All experiments have a “solution vocabulary” and a “guess vocabulary”. The solution vocabulary is the set of all puzzle solutions in the experiment. The guess vocabulary is the vocabulary that the guessing algorithm picks from to narrow down possible solutions.

In the first experiment,  both the guess vocabulary and the solution vocabulary are the small vocabulary (2,315 past and future Wordle solutions).

The second experiment uses the small vocabulary for its solution vocabulary. The guess vocabulary is the large vocabulary (12,972 words accepted as guesses by Wordle).

The third experiment uses the large vocabulary for both the guess vocabulary and the solution vocabulary.

## Results

In all experiments, every algorithm performs better than the random baseline. The difference in performance is most noticeable when a large guess vocabulary is used in Experiments 2 and 3. In these experiments, the win rate of the algorithms exceeds the random baseline by at least 3.45%, and the algorithms average at least 0.43 fewer guesses per game.

The performance of the algorithms in relation to each other is also consistent across experiments. The EntropyGuesser has the highest win rates and lowest average guesses, followed by the MinVocabGuesser. The SimilarityGuesser has the worst performance of the algorithms, although it still performs distinctly better than the random baseline. 

Algorithm efficiency was compared by measuring the average guessing time per game in Experiment 3. The EntropyGuesser, SimilarityGuesser and random baseline all had a roughly similar average guessing time (0.029-0.044 seconds), while the MinVocabGuesser took roughly ten times as long to complete each game (averaging 0.335 seconds).

### Experiment 1:

| Guesser type | Average guesses | Win rate |
| :--- | ---: | ---: |
| Random baseline (WordleGuesser) | 4.08 | 98.57% |
| Entropy (EntropyGuesser) | 3.61 | 99.48% |
| Similarity (SimilarityGuesser) | 3.62 | 99.35% |
| Min. vocabulary (MinVocabGuesser) | 3.63 | 99.4% |

Guesser performance on small target vocabulary with small guess vocabulary

### Experiment 2:

| Guesser type | Average guesses | Win rate |
| :--- | ---: | ---: |
| Random baseline (WordleGuesser) | 4.91 | 90.5% |
| Entropy (EntropyGuesser) | 4.26 | 95.94% |
| Similarity (SimilarityGuesser) | 4.42 | 93.95% |
| Min. vocabulary (MinVocabGuesser) | 4.36 | 95.03 % |

Guesser performance on small target vocabulary  with large guess vocabulary

### Experiment 3:

| Guesser type | Average guesses | Win rate |
| :--- | ---: | ---: |
| Random baseline (WordleGuesser) | 5.14 | 84.45% |
| Entropy (EntropyGuesser) | 4.58 | 90.82% |
| Similarity (SimilarityGuesser) | 4.71 | 89.08% |
| Min. vocabulary (MinVocabGuesser) | 4.65 | 89.99% |

Guesser performance on large target vocabulary with large guess vocabulary

### Algorithm efficiency:

| Guesser type | Mean guessing time per game (in seconds) | 
| :--- | ---: |
| Random baseline (WordleGuesser) | 0.029 |
| Entropy (EntropyGuesser) | 0.031 |
| Similarity (SimilarityGuesser) | 0.044 |
| Min. vocabulary (MinVocabGuesser) | 0.335 |

Average guessing speed on large target vocabulary with large guess vocabulary

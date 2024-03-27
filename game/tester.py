# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 16:59:36 2022

This file contains the WordleTester class, which tests the number of guesses
a WordleGuesser takes to correctly guess each word in a vocabulary. Results of
testing are written to an output file.

@author: Nora Goldfine
"""

from wordle_guesser import WordleGuesser
from collections import defaultdict 
import time

class WordleTester:
    
    WORD_LENGTH = 5
    
    def __init__(self, guesser, vocab, writer, max_guesses=6):
        self.guesser = guesser
        self.vocab = sorted(vocab)
        self.writer = writer
        self.max_guesses = max_guesses
        
    def success(self, guess_counts, guesses, total_guesses, wins, win_guesses):
        guess_counts[guesses] += 1
        total_guesses += guesses
        self.writer.write(f'\nguesses: {guesses}\n\n')
        if guesses <= self.max_guesses:
            wins += 1
            win_guesses += guesses
        return total_guesses, wins, win_guesses
    
    def letter_count(self, word, letter):
        count = 0
        for x in word:
            if x == letter:
                count += 1
        return count

    def letter_matches(self, target, guess, letter, start_index):
        count = 0
        for i in range(start_index, len(guess)):
            if guess[i] == letter and target[i] == letter:
                count += 1
        return count
    
    def try_again(self, guess, target):
        feedback = [WordleGuesser.GRAY] * WordleTester.WORD_LENGTH
        for i in range(len(guess)):
            #print(f'guess[i]= {guess[i]} \t target[i]= {target[i]}')
            if guess[i] == target[i]:
                feedback[i] = WordleGuesser.GREEN
        for i in range(len(guess)):
            if feedback[i] != WordleGuesser.GREEN and guess[i] in target:
                so_far = self.letter_count(guess[:i+1], guess[i])
                later_threes = self.letter_matches(target, guess, guess[i], i+1)
                confirmed = so_far + later_threes
                if confirmed <= self.letter_count(target, guess[i]):
                    feedback[i] = WordleGuesser.GOLD
        self.writer.write(f'{feedback} ')
        self.writer.flush()
        hint = ''.join(feedback)
        self.guesser.filt(hint)
        self.writer.write(f'{len(self.guesser.words)}')
        
    def test_word(self, target, guess_counts, total_guesses, wins, win_guesses, 
                  total_failures):
        self.writer.write(f'target: {target}')
        guessed = False
        guesses = 0
        guess = None
        
        while not guessed:
            guesses += 1
            new_guess = self.guesser.make_guess()
            if new_guess == guess:
                self.writer.write('\n\n')
                self.writer.write(f'Scores: {self.guesser.scores}\n')
                raise Exception(f'ERROR -- Guess the same as previous guess: {guess}; Solved guessers: {[x.is_solved() for x in self.guesser.guessers]}')
            else:
                guess = new_guess
            self.writer.write(f'\n\t{guess} ')
            
            if guess == target:
                guessed = True
                total_guesses, wins, win_guesses = self.success(guess_counts, 
                                                                guesses, 
                                                                total_guesses, 
                                                                wins, 
                                                                win_guesses)
            
            elif guess == None:
                self.writer.write('\nUNABLE TO FIND WORD\n\n')
                total_failures += 1
                guessed = True
                
            else:
                self.try_again(guess, target)
        
        return total_guesses, wins, win_guesses
            
    def display(self, guess_counts, total_guesses, voc_len, wins, win_guesses, 
                elapsed, total_failures):
        for i in range(1, max(guess_counts)+1):
            self.writer.write(f'guess count: {i} \t number of words {guess_counts[i]}\n')
        
        self.writer.write(f'\naverage guesses: {total_guesses / voc_len}\n\n')
        
        self.writer.write(f'win rate (word found in 6 guesses or less): {wins / voc_len}\n')
        self.writer.write(f'average guesses on won games: {win_guesses / wins}\n\n')
        
        self.writer.write(f'vocabulary did not include solution {total_failures} times\n')
        self.writer.write(f'total failure percentage: {total_failures / voc_len}\n\n')
        
        self.writer.write(f'total guessing time: {elapsed/60} minutes\n')
        self.writer.write(f'time per word: {elapsed / voc_len} seconds')
            
    def test_guesser(self):
        guess_counts = defaultdict(lambda: 0)
        wins = 0
        win_guesses = 0
        total_guesses = 0
        total_failures = 0
        start = time.time()
        
        for i in range(len(self.vocab)):
            target = self.vocab[i]
            if i % 100 == 0:
                now = time.time()
                print(f'{i} {target}: {(now - start) / 60} minutes')
            total_guesses, wins, win_guesses = self.test_word(target, 
                                                              guess_counts, 
                                                              total_guesses, 
                                                              wins, win_guesses, 
                                                              total_failures)
            self.guesser.reset()
            
        end = time.time()
        elapsed = end - start
        
        self.display(guess_counts, total_guesses, len(self.vocab), wins, 
                     win_guesses, elapsed, total_failures)
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 01:21:27 2022

This file contains the MinVocabGuesser class, a subclass of WordleGuesser. 
MinVocabGuesser selects the next guess for a Wordle puzzle by minimizing the 
average remaining vocab after its next guess.

@author: Nora Goldfine
"""

from wordle_guesser import WordleGuesser

class MinVocabGuesser(WordleGuesser):
    
    SMALL_GUESS_FILE = '../processed_data/small_voc.txt'
    LARGE_GUESS_FILE = '../processed_data/large_voc.txt'
    
    def set_early_guesses(guesses_file):
        with open(guesses_file, 'r') as reader:
            lines = reader.readlines()
        
        first = lines[0]
        MinVocabGuesser.first_guess = first.strip()
        
        seconds = lines[1:]
        MinVocabGuesser.second_guesses = dict()
        for line in seconds:
            items = line.split()
            hint, guess = items[0], items[1]
            MinVocabGuesser.second_guesses[hint] = guess
            
    def __init__(self, set_vocab=True, small_vocab=True, set_guesses=True):
        WordleGuesser.__init__(self, set_vocab, small_vocab)
        
        if set_guesses == True:
            if small_vocab == True:
                guesses_file = MinVocabGuesser.SMALL_GUESS_FILE
            else:
                guesses_file = MinVocabGuesser.LARGE_GUESS_FILE 
            MinVocabGuesser.set_early_guesses(guesses_file)
            
        self.guess_count = 0
        
    def reset(self):
        WordleGuesser.reset(self)
        self.guess_count = 0
            
    ### METHODS FOR GUESSING ###
    
    def _filter_by_position(self, guess, target, words):
        for i in range(len(guess)):
            if guess[i] == target[i]:
                for word in list(words):
                    if word[i] != guess[i]:
                        words.remove(word)
            else:
                for word in list(words):
                    if word[i] == guess[i]:
                        words.remove(word)
                        
    def _filter_by_count(self, guess, target, words):
        for letter in self.letter_counts[guess]:
            guess_count = self.letter_counts[guess][letter]
            target_count = self.letter_counts[target][letter]
            if guess_count <= target_count:
                for word in list(words):
                    if self.letter_counts[word][letter] < guess_count:
                        words.remove(word)
            else:
                for word in list(words):
                    if self.letter_counts[word][letter] > target_count:
                        words.remove(word)
    
    def _filtered_length(self, guess, target):
        words = self.words.copy()
        self._filter_by_position(guess, target, words)
        self._filter_by_count(guess, target, words)
        return len(words)
    
    def result_length(self, guess):
        all_lengths = 0
        for target in self.words:
            all_lengths += self._filtered_length(guess, target)
        return all_lengths
    
    def make_guess(self):
        if len(self.words) == 0:
            return None
        
        self.guess_count += 1
        if self.guess_count == 1:
            self.guess = MinVocabGuesser.first_guess
        elif self.guess_count == 2:
            self.guess = MinVocabGuesser.second_guesses[self.hints]
        else:
            self.guess = min(self.words, key=self.result_length)
        return self.guess
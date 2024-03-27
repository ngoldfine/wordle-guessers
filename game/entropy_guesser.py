# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 00:49:14 2022

This file contains the EntropyGuesser class, a subclass of WordleGuesser. 
EntropyGuesser selects the next guess for a Wordle puzzle by maximizing the 
entropy over the different puzzle feedback options ("hints").

@author: Nora Goldfine
"""

from wordle_guesser import WordleGuesser
from collections import defaultdict
import math

class EntropyGuesser(WordleGuesser):
    
    SMALL_GUESS_FILE = '../processed_data/small_ent_guesses.txt'
    LARGE_GUESS_FILE = '../processed_data/large_ent_guesses.txt'
    
    def set_early_guesses(guesses_file):
        with open(guesses_file, 'r') as reader:
            lines = reader.readlines()
        
        first = lines[0]
        EntropyGuesser.first_guess = first.strip()
        
        seconds = lines[1:]
        EntropyGuesser.second_guesses = dict()
        for line in seconds:
            items = line.split()
            hint, guess = items[0], items[1]
            EntropyGuesser.second_guesses[hint] = guess
                
    def __init__(self, set_vocab=True, small_vocab=True, set_guesses=True):
        WordleGuesser.__init__(self, set_vocab, small_vocab)
        
        if set_guesses == True:
            if small_vocab == True:
                guess_file = EntropyGuesser.SMALL_GUESS_FILE
            else:
                guess_file = EntropyGuesser.LARGE_GUESS_FILE
            EntropyGuesser.set_early_guesses(guess_file)
            
        self.guess_count = 0
            
    def reset(self):
        WordleGuesser.reset(self)
        self.guess_count = 0
        
    ### METHODS FOR GUESSING ###
    
    def count_letters(self, word, letter):
        count = 0
        for x in word:
            if x == letter:
                count += 1
        return count

    def match_letters(self, target, guess, letter, start_index):
        count = 0
        for i in range(start_index, len(guess)):
            if guess[i] == letter and target[i] == letter:
                count += 1
        return count
    
    def get_hint(self, guess, target):
        feedback = [WordleGuesser.GRAY] * 5
        
        #add green to feedback
        for i in range(len(guess)):
            if guess[i] == target[i]:
                feedback[i] = WordleGuesser.GREEN
        
        #add gold to feedback
        for i in range(len(guess)):
            if feedback[i] != WordleGuesser.GREEN and guess[i] in target:
                so_far = self.count_letters(guess[:i+1], guess[i])
                later_threes = self.match_letters(target, guess, guess[i], i+1)
                confirmed = so_far + later_threes
                if confirmed <= self.letter_counts[target][guess[i]]:
                    feedback[i] = WordleGuesser.GOLD
                    
        return ''.join(feedback)
    
    def get_hint_counts(self, guess):
        hint_counts = defaultdict(lambda: 0)
        for target in self.words:
            hint = self.get_hint(guess, target)
            hint_counts[hint] += 1
        return hint_counts.values()
    
    def entropy(self, guess):
        ent = 0
        counts = self.get_hint_counts(guess)
        for count in counts:
            if count > 0:
                prob = count / len(self.words)
                logprob = math.log2(prob)
                ent += prob * logprob 
        return -1 * ent
    
    def make_guess(self):
        if len(self.words) == 0:
            raise ValueError('There are no words that match the hints.')
        
        self.guess_count += 1
        if self.guess_count == 1:
            self.guess = EntropyGuesser.first_guess
        elif self.guess_count == 2:
            self.guess = EntropyGuesser.second_guesses[self.hints]
        else:
            self.guess = max(self.words, key=self.entropy)
        return self.guess
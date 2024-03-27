# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 17:16:06 2022

This file contains the WordleGuesser class, solves Wordle puzzles. WordleGuesser
randomly selects a guess from its vocabulary, and filters remaining possible 
guesses based on the letter-color feedback ("hints") a Wordle puzzle provides.  

@author: Nora Goldfine
"""

from collections import defaultdict
import random

class WordleGuesser:
    
    GRAY = '1'
    GOLD = '2'
    GREEN = '3'
    LARGE_VOC_FILE = '../raw_data/wordle_vocab.txt'
    SMALL_VOC_FILE = '../raw_data/wordle_wins.txt'
    SEED = 'WordleGuesser'
    
    def set_vocabulary(vocab_file):
        with open(vocab_file, 'r') as reader:
            lines = reader.readlines()
        vocab = [x.strip() for x in lines if len(x.strip()) == 5]
        WordleGuesser.vocab = set(vocab)
        
    def set_letter_counts():
        WordleGuesser.letter_counts = defaultdict(lambda: defaultdict(lambda: 0))
        for word in WordleGuesser.vocab:
            for letter in word:
                WordleGuesser.letter_counts[word][letter] += 1
    
    def __init__(self, set_vocab=True, small_vocab=True):
        
        #get initial vocabulary
        if set_vocab == True:
            vocab_file = WordleGuesser.SMALL_VOC_FILE if small_vocab == True else WordleGuesser.LARGE_VOC_FILE
            WordleGuesser.set_vocabulary(vocab_file)
            WordleGuesser.set_letter_counts()
        self.words = WordleGuesser.vocab.copy()
        self.letter_counts = WordleGuesser.letter_counts.copy()
        
        #minimum number of times letter must occur in target word
        self.min_counts = defaultdict(lambda: 0)
        
        #will be set to True correct word is guessed (when vocab is filtered 
        #using hint '33333')
        self.solved = False 
        
        #set random seed for random guessing
        random.seed(WordleGuesser.SEED)
    
    def reset(self):
        self.words = WordleGuesser.vocab.copy()
        self.letter_counts = WordleGuesser.letter_counts.copy()
        self.min_counts = defaultdict(lambda: 0)
        self.solved = False
        
    def is_solved(self):
        return self.solved
    
    #METHODS FOR GUESSING
    
    def make_guess(self):
        self.guess = random.choice(list(self.words))
        return self.guess
    
    #METHODS FOR FILTERING POSSIBLE WORDS
    
    def _update_min_counts(self):
        """Based on hints, update minimum number of times letters must appear 
        in guesses."""
        gold_green = defaultdict(lambda: 0)
        for i in range(len(self.guess)):
            if self.hints[i] == WordleGuesser.GREEN or self.hints[i] == WordleGuesser.GOLD:
                letter = self.guess[i]
                gold_green[letter] += 1
        for letter in gold_green:
            self.min_counts[letter] = gold_green[letter]
            
    def _filter_gray(self, word, letter):
        if self.letter_counts[word][letter] <= self.min_counts[letter]:
            return True
        return False
    
    def _filter_gold(self, word, letter, index):
        if word[index] != letter and (self.letter_counts[word][letter] >= 
                                      self.min_counts[letter]):
            return True
        return False
    
    def _filter_green(self, word, letter, index):
        if word[index] == letter:
            return True
        return False
    
    def _keep_word(self, word):
        keep = True
        for i in range(len(self.hints)):
            try:
                letter = self.guess[i]
            except IndexError:
                raise IndexError(f'String index out of range -- guess: {self.guess}, hint: {self.hints}, index: {i}')
            if self.hints[i] == WordleGuesser.GRAY:
                keep = self._filter_gray(word, letter)
            elif self.hints[i] == WordleGuesser.GOLD:
                keep = self._filter_gold(word, letter, i)
            elif self.hints[i] == WordleGuesser.GREEN:
                keep = self._filter_green(word, letter, i)
            
            if keep == False:
                break
        
        return keep
    
    def filt(self, hints):
        """Filter possible guesses based on hint (a string)."""
        self.hints = hints
        self._update_min_counts()
        
        for word in list(self.words):
            if self._keep_word(word) == False:
                self.words.remove(word)
                
        if self.hints == WordleGuesser.GREEN * 5:
            self.solved = True
            self.words = set() #no words left to guess
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 15:29:48 2022

This file contains the SimilarityGuesser class, a subclass of WordleGuesser. 
SimilarityGuesser selects the next guess for a Wordle puzzle by minimizing the 
edit distance of its guess from all other possible guesses.

@author: Nora Goldfine
"""

from wordle_guesser import WordleGuesser

class SimilarityGuesser(WordleGuesser):
    
    SMALL_GUESS_FILE = '../processed_data/small_sim_guesses.txt'
    LARGE_GUESS_FILE = '../processed_data/large_sim_guesses.txt'
    
    def set_early_guesses(guesses_file):
        with open(guesses_file, 'r') as reader:
            lines = reader.readlines()
        
        first = lines[0]
        SimilarityGuesser.first_guess = first.strip()
        
        seconds = lines[1:]
        SimilarityGuesser.second_guesses = dict()
        for line in seconds:
            items = line.split()
            hint, guess = items[0], items[1]
            SimilarityGuesser.second_guesses[hint] = guess
    
    def __init__(self, set_vocab=True, small_vocab=True, set_guesses=True):
        WordleGuesser.__init__(self, set_vocab, small_vocab)
        
        if set_guesses == True:
            if small_vocab == True:
                guess_file = SimilarityGuesser.SMALL_GUESS_FILE
            else:
                guess_file = SimilarityGuesser.LARGE_GUESS_FILE
            SimilarityGuesser.set_early_guesses(guess_file)
            
        self.guess_count = 0
            
    def reset(self):
        WordleGuesser.reset(self)
        self.guess_count = 0
        
    ### METHODS FOR GUESSING ###
    
    def similarity_by_quantity(self, word1, word2):
        """Return number of letters shared by word1 and word2, where location
        within each word doesn't matter."""
        score = 0
        for letter in self.letter_counts[word1]:
            score += min(self.letter_counts[word1][letter], 
                         self.letter_counts[word2][letter])
        return score

    def similarity_by_position(self, word1, word2):
        """Return number of letters shared by word1 and word2, where location 
        within each word matters."""
        score = 0
        for i in range(len(word1)):
            if word1[i] == word2[i]:
                score += 1
        return score

    def word_similarity(self, word1, word2):
        """Calculate similarity of word1 and word2. Similarity can be described 
        as m - d, where m is the maximum possible minimum edit distance between 
        two words with the same length as word1 and word2, and d is the minimum 
        edit distance between word1 and word2."""
        score = self.similarity_by_quantity(word1, word2)
        if score > 0:
            score += self.similarity_by_position(word1, word2)
        return score
    
    def global_similarity(self, guess):
        score = 0
        for target in self.words:
            score += self.word_similarity(guess, target)
        return score
    
    def make_guess(self):
        if len(self.words) == 0:
            return None
        
        self.guess_count += 1
        if self.guess_count == 1:
            self.guess = SimilarityGuesser.first_guess
        elif self.guess_count == 2:
            self.guess = SimilarityGuesser.second_guesses[self.hints]
        else:
            self.guess = max(self.words, key=self.global_similarity)
        return self.guess
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 18:35:56 2022

Driver for testing WordleGuesser (and its subclasses SimilarityGuesser, 
EntropyGuesser and MinVocabGuesser) using the WordleTester class.

Guessers are evaluated using two vocabularies. The smaller vocabulary is the set
of all past and future official Wordle puzzle solutions. The larger vocabulary
is the set of all words that are valid guesses in Wordle. For each guesser 
(WordleGuesser, SimilarityGuesser, EntropyGuesser and MinVocabGuesser), three 
experiments are run:
    1.  The guesser uses the SMALL vocabulary to solve puzzles, and each word
        in the SMALL vocabulary is a puzzle solution. Results are output to files
        ending in "small_small.txt"
    2.  The guesser uses the LARGE vocabulary to solve puzzles, and each word
        in the SMALL vocabulary is a puzzle solution. Results are output to files
        ending in "large_small.txt"
    3.  The guesser uses the LARGE vocabulary to solve puzzles, and each word
        in the LARGE vocabulary is a puzzle solution. Results are output to files
        ending in "large_large.txt"

@author: Nora Goldfine
"""

import os

from tester import WordleTester 
from wordle_guesser import WordleGuesser 
from similarity_guesser import SimilarityGuesser
from entropy_guesser import EntropyGuesser
from min_vocab_guesser import MinVocabGuesser

LARGE_VOC_FILE = '../raw_data/wordle_vocab.txt' # full Wordle vocabulary
SMALL_VOC_FILE = '../raw_data/wordle_wins.txt' # all past and future Wordle puzzle solutions

def get_vocab(vocab_file):
    with open(vocab_file, 'r') as reader:
        lines = reader.readlines()
    vocab = [x.strip() for x in lines if len(x.strip()) == 5]
    return sorted(vocab)

def test(guesser, vocab, output_file):
    print(output_file.upper())
    with open(output_file, 'w') as writer:
        t = WordleTester(guesser, vocab, writer)
        t.test_guesser()

def main():
    
    small_vocab = get_vocab(SMALL_VOC_FILE)
    large_vocab = get_vocab(LARGE_VOC_FILE)
    outloc = '../test_output'
    
    name2guesser = {'random'     : WordleGuesser,
                    'entropy'    : EntropyGuesser,
                    'similarity' : SimilarityGuesser,
                    'minvocab'   : MinVocabGuesser}
    
    # guesses: small vocab, targets: small vocab
    for name in name2guesser:
        guesser_type = name2guesser[name]
        out_file = os.path.join(outloc, name + '_small_small.txt')
        guesser = guesser_type(small_vocab=True)
        test(guesser, small_vocab, out_file)
    
    # guesses: large vocab, targets: small vocab
    for name in name2guesser:
        guesser_type = name2guesser[name]
        out_file = os.path.join(outloc, name + '_large_small.txt')
        guesser = guesser_type(small_vocab=False)
        test(guesser, small_vocab, out_file)
        
    # guesses: large vocab, targets: large vocab
    for name in name2guesser:
        guesser_type = name2guesser[name]
        out_file = os.path.join(outloc, name + '_large_large.txt')
        guesser = guesser_type(small_vocab=False)
        test(guesser, large_vocab, out_file)

if __name__ == '__main__':
    main()
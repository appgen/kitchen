#!/usr/bin/env python2

def sentence_word_counts(tokenized_sentence):
    word_counts = {}
    for token in tokenized_sentence:
        if token[1] not in word_counts:
            word_counts[token[1]] = {}
        word_counts[token[1]][token[0]] = 1 + word_counts[token[1]].get(token[0], 0)
    return word_counts

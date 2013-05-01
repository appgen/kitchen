#!/usr/bin/env python2
from collections import Counter
from random import choice

import nltk

from collabfinder import answers

def _parse(text):
    '''
    Convert the raw text into POS-tagged tokens,
    starting with the token ('', '^') to indicate
    the beginning of the text.

    Also produce a frequency distribution of the tokens.

    Do not split the text into sentences.
    '''
    sequence = []
    counts = Counter()
    for sent in nltk.sent_tokenize(text):
        # Sequence of parts of speech
        tokens = nltk.pos_tag(nltk.word_tokenize(sent))
        for token in tokens:
            sequence.append(token[1])

        # Word counts
        counts.update((t[1] for t in tokens))

    return {
        'sequence': ['^'] + sequence,
        'frequencies': counts
        }

def _build_standard_corpus():
    '''
    Generate strings of raw text from Collabfinder, recruiter forms,
    tech cofounder websites, news articles about apps, &c.
    (Return a generator of strings.)
    '''

def _build_app_corpus(keywords):
    '''
    Use the keywords to find related Wikipedia articles, and return a generator of strings.
    '''

def _build_collabfinder_what_sequences():
    for a in answers():
        if a['description'] and a['description']['what']:
            yield _parse(a['description']['what'])['sequence']

# Intermediary helpers
from pandas import DataFrame
import numpy
from copy import copy
def weighted_random_choser(c):
    '''
    param c:
    type c: collections.Counter
    '''

    p = []
    word = []
    for k,v in c.items():
        p.append(k)
        word.append(v)

    cdf

def _probabilities(raw_text_generator, weight = 1)
    'Produce a probability distribution of words.'
    c = reduce(
        lambda a,b: a + b,
        (_parse(t)['frequencies'] for t in raw_text_generator())
    )
    n = float(sum(c.values()))
    for k,v in c.items():
        c[k] = weight * v / n
    return c

def _choose_next_word():
    raise NotImplementedError('Rewrite this using nltk ngram model.')

# Call these functions from the other file.
def app_what(keywords):
    sequence = choice(list(_build_collabfinder_what_sequences()))
    probabilities = _probabilities(_build_standard_corpus(), weight = 0.5) + \
        _probabilities(_build_app_corpus(keywords), weight = 0.5)

def app_goal(keywords):
    pass

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
def _probabilities(keywoards)
    standard_frequencies = reduce(
        lambda a,b: a + b,
        (_parse(t)['frequencies'] for t in _build_standard_corpus())
    )
    special_frequencies = reduce(
        lambda a,b: a + b,
        (_parse(t)['frequencies'] for t in _build_standard_corpus())
    )
    raise NotImplementedError('Weight the frequencies, and then make probabilties.')

# Call these functions from the other file.
def app_what(keywoards):
    sequence = choice(list(_build_collabfinder_what_sequences()))

def app_goal(keywoards):
    pass

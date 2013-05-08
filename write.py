#!/usr/bin/env python2
'''
Write copy about the app. References:
* http://www.slideshare.net/ogrisel/nltk-scikit-learnpyconfr2010ogrisel
* https://gist.github.com/322906/90dea659c04570757cccf0ce1e6d26c9d06f9283
* http://stackoverflow.com/questions/5708352/named-entity-recognition-for-nltk-in-python-identifying-the-ne
* http://nltk.googlecode.com/svn/trunk/doc/book/ch07.html
* https://github.com/tlevine/crawl-collabfinder
'''

import re
from string import ascii_letters

from random import normalvariate, choice

from numpy import array

from nltk.tokenize import wordpunct_tokenize #, word_tokenize, sent_tokenize
from nltk.probability import LidstoneProbDist #LaplaceProbDist
from nltk import NgramModel
import nltk

import collabfinder

LEFT = '(['
def detokenize(tokens):
    text = ''
    for token in tokens:
        if token[0] in (ascii_letters + LEFT):
            # Add a space
            text += ' '
        elif token[0] in LEFT:
            # Remove a space
            text = text[:-1]

        text += token
    return re.sub(r'\.[^.]*$', '.', text[1:])

MINIMUM_DESCRIPTION_LENGTH = 120
def description_length_func(subdescriptions):
    'Create a function that chooses the length of a description.'
    a = array([len(d) for d in subdescriptions])
    mean = a.mean()
    std = a.std()
    def description_length():
        l = normalvariate(mean, std)
        return int(max(MINIMUM_DESCRIPTION_LENGTH, l))
    return description_length

def train_subdescription(subdescriptions):
    '''
    :param subdescriptions: a list of training texts
    :type subdescriptions: list(list(str))
    '''
    train = [wordpunct_tokenize(d) for d in subdescriptions]
    lm = NgramModel(2, train, estimator = (lambda fdist, bins: LidstoneProbDist(fdist, 0.2)))

    length = description_length_func(subdescriptions)

    return lm, length

import os
import json
def build_generators():
    'Build the text-generation functions.'
    descriptions = filter(None, [project['description'] for project in collabfinder.answers()])
    generators={}
    for key in ['what', 'why', 'need']:
        subdescriptions = [d[key] for d in descriptions]
        lm, length = train_subdescription(subdescriptions)
        generators[key] = lambda about: detokenize(lm.generate(length(), wordpunct_tokenize(about)))

    return generators

def generate(generator, description, key):
    '''
    key: what/why/need
        Which section of collabfinder
    '''
    return generator[key](description)

if __name__ == '__main__':
    g = build_generators()
    d = '''
The word "plumber" dates from the Roman Empire.[2] In Roman times lead was known as plumbum in Latin (hence the abbreviation of 'Pb' for lead on the periodic table of the elements). Roman roofs used lead in conduits and drain pipes[3] and some were also covered with lead, lead was also used for piping and for making baths.[4] In medieval times anyone who worked with lead was referred to as a plumber as can be seen from an extract of workmen fixing a roof in Westminster Palace and were referred to as plumbers "To Gilbert de Westminster, plumber, working about the roof of the pantry of the little hall, covering it with lead, and about various defects in the roof of the little hall".[5] Thus a person with expertise in working with lead was first known as a Plumbarius which was later shortened to plumber.
    '''.split('.')[0]
    print generate(g, d, 'why')


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

from random import normalvariate

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
    lm = NgramModel(3, train, estimator = (lambda fdist, bins: LidstoneProbDist(fdist, 0.2)))

    length = description_length_func(subdescriptions)

    return lm, length

def something():
    sentences = []
    for a in collabfinder.answers():
        if a['description']:
            sentences.extend(nltk.sent_tokenize(a['description']['what']))

    tagged = (nltk.pos_tag(nltk.word_tokenize(sentence)) for sentence in sentences)
    chunked = nltk.batch_ne_chunk(tagged, binary = True)
    for tree in chunked:
        print '---'
        print unicode(tree)
        print extract_entity_names(tree)

def extract_entity_names(tree):
    entity_names = []
    if hasattr(tree, 'node') and tree.node:
        if tree.node == 'NE':
            entity_names.append(' '.join([child[0] for child in tree]))
        else:
            for child in tree:
                entity_names.extend(extract_entity_names(child))
    return entity_names

from nltk.model.api import ModelI
class CollabfinderModel(ModelI):
    'http://nltk.org/_modules/nltk/model/ngram.html#NgramModel'
    pass

if __name__ == '__main__':
    import os
    import json

    descriptions = filter(None, [project['description'] for project in collabfinder.answers()])
    generators={}
    for key in ['what', 'why', 'need']:
        subdescriptions = [d[key] for d in descriptions]
        lm, length = train_subdescription(subdescriptions)
        generators[key] = lambda about: detokenize(lm.generate(length(), wordpunct_tokenize(about)))

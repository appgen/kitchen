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

import nltk
from nltk.model import NgramModel

import collabfinder

LEFT = '(['
def detokenize(tokens):
    text = ''
    for token in tokens:
        word = token[0] # token[1] is pos
        if word[0] in (ascii_letters + LEFT):
            # Add a space
            text += ' '
        elif word[0] in LEFT:
            # Remove a space
            text = text[:-1]

        text += word
    return re.sub(r'\.[^.]*$', '.', text[1:])

def train_subdescription(subdescriptions):
    '''
    :param subdescriptions: a list of training texts
    :type subdescriptions: list(list(str))
    '''
    train = [nltk.pos_tag(nltk.wordpunct_tokenize(d)) for d in subdescriptions]
    lm = NgramModel(3, train, estimator = (lambda fdist, bins: nltk.LidstoneProbDist(fdist, 0.2)))
    return lm

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

from nltk.model.api import ModelI
class CollabfinderModel(ModelI):
    'http://nltk.org/_modules/nltk/model/ngram.html#NgramModel'
    pass

if __name__ == '__main__':
    import os
    import json

    descriptions = filter(None, [project['description'] for project in collabfinder.answers()])
    models = {}
    for key in ['what', 'why', 'need']:
        subdescriptions = [d[key] for d in descriptions]
        models[key] = train_subdescription(subdescriptions)

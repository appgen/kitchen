#!/usr/bin/env python2
'''
Write copy about the app. References:
* http://www.slideshare.net/ogrisel/nltk-scikit-learnpyconfr2010ogrisel
* https://gist.github.com/322906/90dea659c04570757cccf0ce1e6d26c9d06f9283
* http://stackoverflow.com/questions/5708352/named-entity-recognition-for-nltk-in-python-identifying-the-ne
* http://nltk.googlecode.com/svn/trunk/doc/book/ch07.html
* https://github.com/tlevine/crawl-collabfinder


# Ideas
chunked = nltk.batch_ne_chunk(tagged, binary = True)

'''

import re
from string import ascii_letters

import nltk
import nltk.model

import collabfinder

LEFT = '(['
def dewordize(words):
    'Turn a list of words and punctuation into a string.'
    text = ''
    for word in words:
        if word[0] in (ascii_letters + LEFT):
            # Add a space
            text += ' '
        elif word[0] in LEFT:
            # Remove a space
            text = text[:-1]

        text += word
    return re.sub(r'\.[^.]*$', '.', text[1:])

def annotate_first_sentence(subdescriptions):
    '''
    Build an n-gram model of the first sentence.
    :param subdescription: a list of "what", "why" or "need" string
    :type subdescription: list(unicode)
    '''
    return (nltk.pos_tag(nltk.word_tokenize(nltk.sent_tokenize(subdescription)[0])) for subdescription in subdescriptions)

def annotate_full_subdescription(subdescriptions):
    '''
    :param subdescriptions: a list of training texts
    :type subdescriptions: list(unicode)
    '''
    return (nltk.pos_tag(nltk.wordpunct_tokenize(subdescription)) for subdescription in subdescriptions)

def ngram_model(annotation):
    'Build a model given a the pos-tagged annotation.'
    m = nltk.model.NgramModel(3, train, estimator = (lambda fdist, bins: nltk.LidstoneProbDist(fdist, 0.2)))
    return m

def get_subdescriptions():
    import os
    import json

    descriptions = filter(None, [project['description'] for project in collabfinder.answers()])
    subdescriptions = {}
    for key in ['what', 'why', 'need']:
        subdescriptions[key] = [d[key].strip() for d in descriptions]
    return subdescriptions

if __name__ == '__main__':
    models[key] = train_subdescription(subdescriptions)

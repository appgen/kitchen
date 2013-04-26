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

import random
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
    return [nltk.pos_tag(nltk.word_tokenize(nltk.sent_tokenize(subdescription)[0])) for subdescription in subdescriptions]

def annotate_full_subdescription(subdescriptions):
    '''
    :param subdescriptions: a list of training texts
    :type subdescriptions: list(unicode)
    '''
    return [nltk.pos_tag(nltk.wordpunct_tokenize(subdescription)) for subdescription in subdescriptions]

def ngram_model(n, annotation):
    'Build a model given a the pos-tagged annotation.'
    m = nltk.model.NgramModel(n, annotation, estimator = (lambda fdist, bins: nltk.LidstoneProbDist(fdist, 0.2)))
    return m

def is_sentence_end(token):
    return token[0] in '.?!'

def model_subdescription(subdescriptions):
    m1 = ngram_model(2, annotate_first_sentence(subdescriptions))
    m2 = ngram_model(3, annotate_full_subdescription(subdescriptions))
    return m1, m2

def generate_subdescription(m1, m2):
    first_sentence = list(take_until(is_sentence_end, m1.generate(100)))
    more = reversed(m2.generate(300, context = first_sentence))
    return list(reversed(list(remove_until(is_sentence_end, more))))

def remove_until(f, iterable):
    'Take until the condition is matched'
    for i in iterable:
        if f(i):
            yield i
            break
    for i in iterable:
        yield i

def take_until(f, iterable):
    'Take until the condition is matched'
    for i in iterable:
        yield i
        if f(i):
            break

def get_subdescriptions():
    import os
    import json

    descriptions = filter(None, [project['description'] for project in collabfinder.answers()])
    subdescriptions = {}
    for key in ['what', 'why', 'need']:
        subdescriptions[key] = [d[key].strip() for d in descriptions]
    return subdescriptions


def to_grammar(texts):
    'Convert a paragraph or whatnot into a bunch of sentence grammars.'
    sentence_chunk_parses = []
    counts = {}
    for text in texts:
        for sent in nltk.sent_tokenize(text):
            tokens = nltk.pos_tag(nltk.word_tokenize(sent))

            sentence_chunk_parses.append(sentence_chunk_parse(tokens))

            new_counts = sentence_word_counts(tokens)
            for pos,v in new_counts.items():
                for word,c in v.items():
                    if pos not in counts:
                        counts[pos] = {}
                    counts[pos][word] = counts[pos].get(word, 0) + 1
    return sentence_chunk_parses, counts

def sentence_chunk_parse(tokenized_sentence):
    return [token[1] for token in tokenized_sentence]

def sentence_word_counts(tokenized_sentence):
    word_counts = {}
    for token in tokenized_sentence:
        if token[1] not in word_counts:
            word_counts[token[1]] = {}
        word_counts[token[1]][token[0]] = 1 + word_counts[token[1]].get(token[0], 0)
    return word_counts

def expand_word_counts(word_counts):
    'Expand the word counts to repeat the words so we can stupidly random.sample'
    for word,count in word_counts.items():
        for i in range(count):
            yield word

def from_grammar(sentence_chunk_parses, counts):
    'Generate a sentence from the grammar.'
    for pos in random.choice(sentence_chunk_parses):
        yield random.choice(list(expand_word_counts(counts[pos])))

if __name__ == '__main__':
    s = get_subdescriptions()
    m1, m2 = model_subdescription(s['why'])
    def go(m1, m2):
        return dewordize([p[0] for p in generate_subdescription(m1, m2)])

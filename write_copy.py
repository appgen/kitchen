#!/usr/bin/env python2
import nltk
import copy_helpers

def _parse(text):
    '''
    Convert the raw text into POS-tagged tokens,
    starting with the token ('', '^') to indicate
    the beginning of the text.

    Also produce a frequency distribution of the tokens.

    Do not split the text into sentences.
    '''
    sequence = []
    counts = {}
    for sent in nltk.sent_tokenize(text):
        # Sequence of parts of speech
        tokens = nltk.pos_tag(nltk.word_tokenize(sent))
        for token in tokens:
            sequence.append(token[1])

        # Word counts
        new_counts = copy_helpers.sentence_word_counts(tokens)
        for pos,v in new_counts.items():
            for word,c in v.items():
                if pos not in counts:
                    counts[pos] = {}
                counts[pos][word] = counts[pos].get(word, 0) + 1

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

def _collabfinder_goal_corups():
    '''
    Generate strings of raw text from Collabfinder goals.
    '''

# Call these functions from the other file.
def app_description(keywords):
    pass

def app_goal(keywoards):
    pass

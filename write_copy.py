#!/usr/bin/env python2
import nltk


def parse(text):
    '''
    Convert the raw text into POS-tagged tokens,
    starting with the token ('', '^') to indicate
    the beginning of the text.

    Also produce a frequency distribution of the tokens.

    Do not split the text into sentences.
    '''
    sentence_chunk_parses = []
    counts = {}
    for sent in nltk.sent_tokenize(text):
        tokens = nltk.pos_tag(nltk.word_tokenize(sent))

        sentence_chunk_parses.extend(sentence_chunk_parse(tokens))

        new_counts = sentence_word_counts(tokens)
        for pos,v in new_counts.items():
            for word,c in v.items():
                if pos not in counts:
                    counts[pos] = {}
                counts[pos][word] = counts[pos].get(word, 0) + 1
    return {
        'sequence': sentence_chunk_parses,
        'frequencies': counts
        }

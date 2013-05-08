# Mostly taken from the pantry, but separated to make the pipeline
import os, json, re
from unidecode import unidecode

_ONLY_LETTERS = re.compile(r'^[a-z]+$', flags = re.IGNORECASE)
def only_letters(word):
    return re.match(_ONLY_LETTERS, word)

VIEWS = os.path.join('pantry', 'socrata', 'views')
def _get_keywords(viewid):
    'Pick the topic words for a particular view.'
    view = json.load(open(os.path.join(VIEWS, viewid)))

    column_words = []
    for c in view['columns']:
        column_words.extend(c['name'].split(' '))

    words_list = column_words + view.get('tags', []) + view['name'].split(' ') + \
        view.get('description', '').split(' ') + [view.get('category', '')]

    return set(filter(only_letters, set([unidecode(w.lower()) for w in words_list])))

def get_keywords(viewids):
    return reduce(lambda a,b: a.union(b), (_get_keywords(viewid) for viewid in viewids), set())


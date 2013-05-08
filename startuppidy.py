#!/usr/bin/env python2
import os, json
import re
import random
from itertools import chain
from urllib import urlencode

import socrata
import write
from keywords import get_keywords

PREFIXES = [u"responsive", u"game", u"beta", u"tech", u"digital", u"social", u"my", u"our", u"the", u"all", u"in", u"on"]
SUFFIXES = [u"box", u"grid", u"share", u"wise", u"hop", u"works", u"bit", u"book", u"list", u"square", u"rock", u"ly", u"sy", u"er", u"it", u"ie", u"io", u"am", u"ia", u"ora", u"ero", u"ist", u"ism", u"ium", u"ble", u"ify", u"ous", u"ing"]

def _not_nyc_department(tag):
    'Check whether a tag is a word.'
    return tag not in {u'dob'}

def _app_name(tags):
    if len(tags) == 0:
        raise ValueError

    good_tags = filter(_not_nyc_department, tags)
    tag = random.sample(good_tags, 1)[0]
    construction_scheme = random.randint(1,3)

    if construction_scheme == 1:
        # Add prefix
        name = random.sample(PREFIXES, 1)[0] + tag.split(' ')[0]

    elif construction_scheme == 2:
        # Add suffix
        name = random.sample(tag.split(' ')[-1] + random.sample(SUFFIXES, 1)[0], 1)[0]

    elif construction_scheme == 3:
        # Remove last vowel
        _reversed_name = ''.join(reversed(list(tag.split(' ')[-1])))
        name = ''.join(reversed(re.sub(r'[aoeui]', '', _reversed_name, count = 1)))

    return name

def article(title):
    'Download the English Wikipedia article of a given title.'
    urlbase = 'en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&'
    params = urlencode({'titles': title.encode('utf-8')})
    h = open(os.path.join('pantry', 'wikipedia', urlbase + params))
    return json.load(h)['query']['pages']['9252']['revisions'][0]['*']

viewdict = socrata.viewdict()
columndict = socrata.columndict()
generators = write.build_generators()
def app(seed):
    # Set the seed
    random.seed(seed)

    # Data dependencies
    column_name = random.choice(columndict.keys())
    dataset_ids = columndict[column_name]

    # The topic of the app
    keywords = get_keywords(dataset_ids)

    # Choose the name
    name = _app_name(keywords)

    # Collabfinder generators
    def seed_text():
        return ' '.join(random.sample(keywords, 3))

    return {
        'name': name,
#       'datasets': list, each element containing the id, title, description, keywords
        'dataset_ids': dataset_ids,
        'logo': None,
        'collabfinder_what': write.generate(generators, seed_text(), 'what'),
        'collabfinder_why': write.generate(generators, seed_text(), 'why'),
        'collabfinder_need': write.generate(generators, seed_text(), 'need'),
    }


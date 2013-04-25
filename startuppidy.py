#!/usr/bin/env python2
import re
import random
from itertools import chain

import socrata

PREFIXES = [u"responsive", u"game", u"beta", u"tech", u"digital", u"social", u"my", u"our", u"the", u"all", u"in", u"on"]
SUFFIXES = [u"box", u"grid", u"share", u"wise", u"hop", u"works", u"bit", u"book", u"list", u"square", u"rock", u"ly", u"sy", u"er", u"it", u"ie", u"io", u"am", u"ia", u"ora", u"ero", u"ist", u"ism", u"ium", u"ble", u"ify", u"ous", u"ing"]

def _not_nyc_department(tag):
    'Check whether a tag is a word.'
    return tag not in {u'dob'}

def _app_name(tags):
    good_tags = filter(_not_nyc_department, tags)
    tag = random.sample(good_tags, 1)[0]
    construction_scheme = random.randint(1,3)

    if construction_scheme == 1:
        # Add prefix
        name = random.sample(PREFIXES, 1)[0] + tag.split(' ')[0]

    elif construction_scheme == 2:
        # Add suffix
        name = random.sample(tag.split(' ')[-1] + random.sample(SUFFIXES, 1)[0])

    elif construction_scheme == 3:
        # Remove last vowel
        _reversed_name = ''.join(reversed(list(tag.split(' ')[-1])))
        name = ''.join(reversed(re.sub(r'[aoeui]', '', _reversed_name, count = 1)))

    return name

views = socrata.views()
columns = socrata.columns()
def app(seed):
    # Set the seed
    random.seed(seed)

    # Data dependencies
    column_name = random.sample(columns, 1)

    # So ugly
    tags = set()
    for view_id in columns[column_name]:
        tags.union(views[view_id]['tags'])

    # Choose the name
    name = _app_name(tags)

    return {
        'name': name,
        'dataset_ids': colums[column_name],
        'logo': None,
    }

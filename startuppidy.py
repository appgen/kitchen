#!/usr/bin/env python2
import random

PREFIXES = [u"responsive", u"game", u"beta", u"tech", u"digital", u"social", u"my", u"our", u"the", u"all", u"in", u"on"]
SUFFIXES = [u"box", u"grid", u"share", u"wise", u"hop", u"works", u"bit", u"book", u"list", u"square", u"rock", u".ly", u"sy", u"er", u".it", u"ie", u".io", u".am", u"ia", u"ora", u"ero", u"ist", u"ism", u"ium", u"ble", u"ify", u"ous", u"ing"]

def _not_nyc_department(tag):
    'Check whether a tag is a word.'
    return tag not in {u'dob'}

def _app_name(seed, tags):
    good_tags = filter(_not_nyc_department, tags)
    random.seed(seed)
    if random.randint(1,3) == 1:
        name = random.sample(PREFIXES, 1)[0] + random.sample(good_tags, 1)[0].split(' ')[0]
    else:
        name = random.sample(good_tags, 1)[0].split(' ')[-1] + random.sample(SUFFIXES, 1)[0]
    return name

def app(seed):
    random.seed(seed)
    return {}

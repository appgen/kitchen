#!/usr/bin/env python2
import re

import socrata
from helpers import cache, flatten

uniondict = socrata.uniondict()
uniondict_broad = socrata.uniondict_broad()
viewdict = socrata.viewdict()
# columndict = socrata.columndict(minmatches = 1)

def wide_format(view):
    'Assume that the dataset is in long format, but return true if it seems wide.'
    years = boroughs = numbers = []
    for c in view['columns']:
        name = c['name']

        year = re.match(r'.*[12][90][0-9][0-9].*', name)
        borough = re.match(r'.*(bronx|manhattan|queens|brooklyn|staten).*', name, flags = re.IGNORECASE)
        number = re.match(r'_[0-9]', name)

        if year:
            years.append(year.group())
        if borough:
            boroughs.append(year.group())
        if number:
            numbers.append(number.group())

    for variable in [years, borough, numbers]:
        if len(variable) > 1:
            return True
    return False

def subsets(_uniondict):
    for schema, viewids in _uniondict.items():
        datasets = [{
            'id': viewdict[viewid]['id'],
            'name': viewdict[viewid]['name'],
            'attribution': viewdict[viewid].get('attribution'),
            'uploader': viewdict[viewid]['owner']['displayName'],
           #'nrow': len(socrata._rows(viewid)),
        } for viewid in viewids]
        title = socrata.combine_titles([viewdict[viewid] for viewid in viewids])
        yield {'title': title, 'schema': schema, 'datasets': datasets}

def subset_statistics():
    n_datasets = len(viewdict)
    n_unionable = sum(map(len, uniondict_broad.values()))
    n_union_result = len(uniondict_broad)
    return n_datasets, n_unionable, n_union_result

if __name__ == '__main__':
    import json
    json.dump(list(subsets(uniondict_broad)), open('comestibles/unionable.json', 'w'))
    # print subset_statistics()

if __name__ == '__main__':
    viewdict = cache('viewdict', socrata.viewdict)
    columndict = cache('columndict', socrata.columndict)
    uniondict = cache('uniondict', socrata.uniondict)
    generators = cache('generators', write.build_generators)

    viewdict = cache('viewdict', socrata.viewdict)
    for viewid, view in viewdict.items():
        viewdict[viewid]['column_matches']

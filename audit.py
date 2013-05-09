#!/usr/bin/env python2
import re

import socrata

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
    output = []
    for schema, viewids in _uniondict.items():
        names = [viewdict[viewid]['name'] for viewid in viewids]
        output.append({'schema': schema, 'names': names})
    return output

if __name__ == '__main__':
    import json
    json.dump(subsets(uniondict_broad), open('comestibles/unionable.json', 'w'))

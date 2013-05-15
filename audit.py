#!/usr/bin/env python2
import re

import socrata
import write
from helpers import cache, flatten

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

def subset_statistics(uniondict_broad):
    n_datasets = len(viewdict)
    n_unionable = sum(map(len, uniondict_broad.values()))
    n_union_result = len(uniondict_broad)
    return n_datasets, n_unionable, n_union_result

# if __name__ == '__main__':
#     import json
#     json.dump(list(subsets(uniondict_broad)), open('comestibles/unionable.json', 'w'))

if __name__ == '__main__':
    # Load the base information.
    viewdict = cache('viewdict', socrata.viewdict)

    # Connect to the database.
    from dumptruck import DumpTruck
    dt = DumpTruck('/tmp/appgen.db', auto_commit = False)
    dt.drop('dataset', if_exists = True)
    dt.create_table(viewdict.values()[0], 'dataset')
    dt.create_index(['id'], 'dataset', if_not_exists = True, unique = True)

    # Add the join references (shared columns).
    columndict = cache('columndict', socrata.columndict)
    for column, new_viewids in columndict.items():
        for viewid in new_viewids:
            old_viewids = set(viewdict[viewid].get('joinable', []))
            viewdict[viewid]['joinable'] = list(old_viewids.union(new_viewids))

    # Add the union references (shared schema)
    uniondict = cache('uniondict', socrata.uniondict)
    for schema, viewids in uniondict.items():
        for viewid in viewids:
            viewdict[viewid]['schema'] = list(schema)
            viewdict[viewid]['unionable'] = list(viewids)

    # uniondict_broad = socrata.uniondict_broad()
    # generators = cache('generators', write.build_generators)


    # Save to the database.
    for view in viewdict.values():
        # There's a lot of interesting stuff in these fields,
        # but they're big or weakly structured.
        # Remove these because they're big
        for key in ['columns', 'metadata', 'displayFormat', 'viewFilters', 'query']:
            del(view[key])

        # Flatten
        dt.insert(flatten(view), 'dataset')
    dt.commit()

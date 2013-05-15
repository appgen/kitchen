#!/usr/bin/env python2
import socrata

from copy import copy
from helpers import cache
from helpers import flatten

def main():

if __name__ == '__main__':
    viewdict = cache('viewdict', socrata.viewdict)
    columndict = cache('columndict', socrata.columndict)
    uniondict = cache('uniondict', socrata.uniondict)
    generators = cache('generators', write.build_generators)

    viewdict = cache('viewdict', socrata.viewdict)
    for viewid, view in viewdict.items():
        viewdict[viewid]['column_matches']

    import json

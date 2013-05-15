#!/usr/bin/env python2
import socrata

from copy import copy
from helpers import cache

def _nested_dict_iter(nested, sep):
    for key, value in nested.iteritems():
        if hasattr(value, 'iteritems'):
            for inner_key, inner_value in _nested_dict_iter(value):
                yield key + sep + inner_key, inner_value
        else:
            yield key, value

def flatten(nested, sep = '.'):
    'Flatten a dictionary, replacing nested things with dots.'
    return dict(_nested_dict_iter(nested, sep))

def main():
    viewdict = cache('viewdict', socrata.viewdict)
    for viewid, view in viewdict.items():
        viewdict[viewid][

if __name__ == '__main__':
    import json

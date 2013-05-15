#!/usr/bin/env python2
import socrata

from copy import copy
from helpers import cache

def flatten(nested_dict, sep = '.'):
    'Flatten a dictionary, replacing nestings with dots or whatnot.'
    d = copy(nested_dict)

def nested_keys(nested_dict, prefix = []):
    for parent_key, parent in nested_dict.items():
        if hasattr(parent, 'items'):
            for child_key in nested_keys(parent, prefix = prefix + [parent_key]):
                yield child_key
        else:
            yield prefix + [parent_key]

def _flatten_pair(key, value):
    if hasattr(value, 'items'):
        return {(key + sep + a):b for a,b in value.items()}
    else:
        return {key:value}


def main():
    viewdict = cache('viewdict', socrata.viewdict)
    for viewid, metadata in viewdict.items():
        metadata.update({
        })
        yield metadata

if __name__ == '__main__':
    import json

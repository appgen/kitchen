#!/usr/bin/env python2
import socrata

from helpers import cache

def flatten(subdict, prefix = None, sep = '.'):
    'Flatten a dictionary, replacing nestings with dots or whatnot.'
    prepend = '' if prefix == None else (prefix + sep)
    if hasattr(subdict, 'items'):
        for parent_key, parent in subdict.items():
            if hasattr(parent, 'items'):
                for child_key, child in parent.items():
                    subdict[parent_key + sep + child_key] = child
                del(subdict[parent_key])
        return {(prepend + k):flatten(v, prefix = k) for k,v in subdict.items()}
    else:
        return subdict


def main():
    viewdict = cache('viewdict', socrata.viewdict)
    for viewid, metadata in viewdict.items():
        metadata.update({
        })
        yield metadata

if __name__ == '__main__':
    import json

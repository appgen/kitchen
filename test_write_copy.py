import nose.tools as n
from collections import Counter

import write_copy

def test_parse():
    observed = write_copy.parse('The boat floated across the river sank.')
    expected = {'frequencies': {
                    '.': {'.': 1},
                    'DT': {'The': 1, 'the': 1},
                    'IN': {'across': 1},
                    'NN': {'boat': 1, 'river': 1, 'sank': 1},
                    'VBD': {'floated': 1}},
                'sequence': ['^', 'DT', 'NN', 'VBD', 'IN', 'DT', 'NN', 'NN', '.']}
    n.assert_dict_equal(observed['frequencies'], expected['frequencies'])
    n.assert_list_equal(observed['sequence'], expected['sequence'])
    n.assert_list_equal(observed.keys(), expected.keys())

def test_cdf():
    '''
    cdf should build a cumulative distribution function of bigram latter halves
    based on a generator of collections.Counter.
    '''
    def example():
        yield Counter('abe')
        yield Counter('aabb')
        yield Counter('acb')

    observed = write_copy.cdf(example(), weight = 1)
    for k,v in observed.items():
        observed[k] = set(v)

    expected = {
        '^': {(1.00, 'a')},
        'a': {(0.25, 'b'),
              (0.75, 'a'),
              (1.00, 'c')},
        'b': {(0.25, 'e'),
              (0.50, 'b'),
              (1.00, '$')},
        'c': {(1.00, 'b')}
        'e': {(1.00, '$')}
        }

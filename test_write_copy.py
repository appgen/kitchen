import nose.tools as n
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

from startuppidy import app
import nose.tools as n

def test_keys():
    'All of the app parameters should be present.'
    observed = set(app(1337).keys())
    expected = {
        'datasets',
    }

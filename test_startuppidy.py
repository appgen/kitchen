import startuppidy
import nose.tools as n

def test_keys():
    'All of the app parameters should be present.'
    observed = set(startuppidy.app(1337).keys())
    expected = {
        # Identity
        'dataset_ids',
        'logo',
        'name',

        # Collabfinder submission
        'collabfinder_what',
        'collabfinder_why',
        'collabfinder_need',
        'background_image',

        # Other copy
        'about',
        'team',

        # Assets
        'stock_photo',

        # Data
        'geojson',
    }
    n.assert_dict_equal(observed, expected)

def test_app_name_should_be_unicode():
    observed = type(startuppidy._app_name(['master plumber', 'education']))
    n.assert_equal(observed, unicode)

def test_app_name_should_not_fail():
    startuppidy._app_name(['abc'])
    startuppidy._app_name(['abc'])
    startuppidy._app_name(['abc'])
    startuppidy._app_name(['abc'])
    startuppidy._app_name(['abc'])
    startuppidy._app_name(['abc'])
    startuppidy._app_name(['abc'])
    startuppidy._app_name(['abc', 'def'])
    startuppidy._app_name(['abc', 'def'])
    startuppidy._app_name(['abc', 'def'])
    startuppidy._app_name(['abc', 'def'])
    startuppidy._app_name(['abc', 'def'])
    startuppidy._app_name(['abc', 'def'])
    startuppidy._app_name(['abc', 'def'])

def test_app_name_should_fail_on_empty_list():
    with n.assert_raises(ValueError):
        startuppidy._app_name([])

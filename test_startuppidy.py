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
    observed = type(startuppidy._app_name(42, ['master plumber', 'education']))
    n.assert_equal(observed, unicode)


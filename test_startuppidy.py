from startuppidy import app
import nose.tools as n

def test_keys():
    'All of the app parameters should be present.'
    observed = set(app(1337).keys())
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

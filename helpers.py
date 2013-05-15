# Some of this comes from hardhat
import os

# Cache
import pickle

def save(key, value, cache_dir = '/tmp/appgen'):
    'Save an object to the cache_dir.'
    cache_path = os.path.join(cache_dir, key + '.p')
    cache_file = open(cache_path, 'wb')
    pickle.dump(value, cache_file)
    cache_file.close()

def load(key, cache_dir = '/tmp/appgen'):
    'Load an object from the cache_dir.'
    cache_path = os.path.join(cache_dir, key + '.p')
    if os.path.exists(cache_path):
        cache_file = open(cache_path, 'rb')
        data = pickle.load(cache_file)
        cache_file.close()
    else:
        raise KeyError(key)
    return data

def cache(key, func, cache_dir = '/tmp/appgen'):
    '''
    Check if a value is in the cache.
    Load and cache it from the function if it isn\'t already cached.
    '''
    cache_path = os.path.join(cache_dir, key + '.p')

    if os.path.exists(cache_path):
        data = load(key, cache_dir = cache_dir)
    else:
        # Run the function
        data = func()

        # Cache
        save(key, data, cache_dir = cache_dir)

    return data

def memoize(key, cache_dir = '/tmp/appgen'):
    '''
    Use this as a decorator.
    Check if a value is in the cache.
    Load and cache it from the function if it isn\'t already cached.
    '''
    def decorator(func):
        def wrapper():
            cache_path = os.path.join(cache_dir, key + '.p')

            if os.path.exists(cache_path):
                data = load(key, cache_dir = cache_dir)
            else:
                # Run the function
                data = func()

                # Cache
                save(key, data, cache_dir = cache_dir)

            return data
        return wrapper
    return decorator


def _nested_dict_iter(nested, sep):
    for key, value in nested.iteritems():
        if hasattr(value, 'iteritems'):
            for inner_key, inner_value in _nested_dict_iter(value, sep):
                yield key + sep + inner_key, inner_value
        else:
            yield key, value

def flatten(nested, sep = '.'):
    'Flatten a dictionary, replacing nested things with dots.'
    return dict(_nested_dict_iter(nested, sep))

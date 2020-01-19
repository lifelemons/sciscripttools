import numpy as np
import logging

# setup logging
logger = logging.getLogger(__name__)

def prepare_json_dictionary(dictionary):
    """
    Prepare a dictionary so that it can be written to a json file.
    
    Convert items within the dictionary to something that can be written to a
    dictionary.
    """

    if not isinstance(dictionary, dict):
        raise Exception("Expected a dictionary object.")

    keys = dictionary.keys()
    for key in keys:
        data = dictionary[key]
        
        if isinstance(data, dict):
            logger.info("Recursive call, dictionary within a dictionary.")
            logger.info("Also preparing %s for writing to a json file.", key)
            data = prepare_json_dictionary(data)
            dictionary[key] = data

        elif isinstance(data, np.ndarray):
            dictionary[key] = data.tolist()

        elif not isinstance(data, np.ndarray):
            data = np.array(data)
            dictionary[key] = data.tolist()
            
        # add other conversions here
    
    return 0

def dictionary_to_arrays(dictionary):
    """
    Convert a dictionary into two arrays of keys and data.
    
    Recurivse function: a dictionary within a dictionary will also
    be converted.
    
    Returns
    -------
    keys : list
        list of all the keys
    data : list
        list of all the corresponding items
    """

    keys = []
    data = []
    
    for key, item in dictionary.items():
        
        if isinstance(item, dict):
            logger.info("Recursive call, dictionary within a dictionary.")
            logger.info("Also converting %s dictionary to arrays.", key)
            key, item = dictionary_to_arrays(item)
        
        keys.append(key)
        data.append(item)

    return keys, data

def dictionary_items_to_numpy_arrays(dictionary):
    """
    Convert array-like items within a dictionary into numpy arrays.
    
    Recurivse function: a dictionary within a dictionary will also
    be converted.
    
    Returns
    -------
    dictionary : dict
        Similar dictionary, now with some items as numpy arrays.
    """
    
    for key, item in dictionary.items():
        
        if isinstance(item, dict):
            logger.info("Recursive call, dictionary within a dictionary.")
            logger.info("Also converting %s dictionary items to numpy arrays.", key)
            item = dictionary_items_to_numpy_arrays(item)
            dictionary[key] = item
        
        else:
            # if not a singular item or a string
            try:
                if len(item) != 1 and isinstance(item, str) == False:
                    try:
                        # convert to a numpy array
                        dictionary[key] = np.array(item)
                    except: 
                        logger.debug("Probably not an array-like item.")
            except:
                logger.debug("Probably a singular item.")

    return 0
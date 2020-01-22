import logging

from .checks import check_argument_pairs
from .arguments import process_arguement_pairs

# setup logging
logger = logging.getLogger(__name__)

def create_dictionary(*args):
    """
    Create a dictionary using a list of keys and corresponding data
    
    Parameters
    ----------
    *args : str, data OR arrays of str and data
        Given as a pair, a string for the key and the data.
        Multiple pairs can be inputted.
        OR arrays of strings and the data.
    
    Returns
    -------
    dict
        Dictionary of the given arguments.
    
    Example
    -------
    create_dictionary("thickness", 0.045)
    create_dictionary("thickness", 0.045, "resistance", 0.0015)
    
    keys = ["thickness", "resistance"]
    data = [0.045, 0.0015]
    create_dictionary(keys, data)
    """
    
    check_argument_pairs(args)
    
    first_arg = args[0]
    
    if len(args) == 2:
        # a singular pair 
        if isinstance(first_arg, str):
            return {first_arg: args[1]}
        
        # might be a pair of arrays that have been passed in
        else: 
            if len(first_arg) >= 1 and isinstance(first_arg[0], str) == True:
                logger.debug("Probably two arrays of items.")
                return dict(zip(args[0], args[1]))
        
    # multiple pairs
    else:
        pairs = process_arguement_pairs(args)
        return dict(pairs)
        
    return 1
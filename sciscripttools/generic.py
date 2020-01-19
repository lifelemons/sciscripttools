import logging

from .checks import check_argument_pairs

# setup logging
logger = logging.getLogger(__name__)

def process_arguement_pairs(arguments):
    """
    Create list of pairs from the arguments.
    
    Parameters
    ----------
    arguments : Tuple
        tuple list of arguments that are passed into a function
    """
    if not isinstance(arguments, tuple):
        message = ("Expected a tuple of arguments.")
        raise Exception(message)
        
    pairs = []
    for i in range(0, int(len(arguments)/2)):
        pairs.append((arguments[(2*i)], arguments[(2*i)+1]))
    
    return pairs

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
        pairs = checks.process_arguement_pairs(args)
        return dict(pairs)
        
    return 1
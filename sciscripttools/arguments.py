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
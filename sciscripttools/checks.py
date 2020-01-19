def check_argument_pairs(arguments, text_suffix ="arguments"):
    """
    Check for correct number of arguments pairs.
    Throw exception if not correct.

    Parameters
    ----------
    arguments : Tuple
        tuple list of arguments that are passed into a function
    """
    if not isinstance(arguments, tuple):
        message = ("Expected a tuple of arguments, "
                   "likely to be a singular argument.")
        raise Exception(message)

    if (len(arguments) % 2) != 0:
        message = ("Incorrect number of arguments, "
                   "need pairs of {}.".format(text_suffix))
        raise Exception(message)

    return 0
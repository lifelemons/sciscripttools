# Input / Ouput Functions

import os
import logging
import json

from .checks import check_argument_pairs
from .arguments import process_arguement_pairs
from .conversion import prepare_json_dictionary
from .generic import create_dictionary

# setup logging
logger = logging.getLogger(__name__)

def prepare_filename(filename, file_format, directory):
    """
    Prepare filename with file format and directory.
    Written for the load_data() and save_data() functions.
    
    Parameters
    ----------
    filename : str
        The file name.
    file_format : str
        The file formart / extension.
    directory : str
        The path for the file.
        
    Returns
    -------
    filename : str
        Full path of the file
        
    """

    # if file format does not exist in filename, add file format
    file_format_in = os.path.splitext(filename)[1]
    if len(file_format_in) == 0:
        filename += file_format

    # add directory to filename
    if directory != "":
        filename = os.path.join(directory, filename)

    return filename

def load_dictionary(*args, keys=[], directory=""):
    """
    Load a dictionary(ies) from a file, or multiple files.
    
    Parameters
    ----------
    *args : str, multiple str, list of str, array of str etc.
        A string, multiple strings, or collection of strings with the 
        filename(s).

    keys : [], list, array, str, optional
        Names of items to load from the file(s).
        Default will load all items from the file(s).
        Can provide a single string to load a single key.
    directory : "", str, optional
        The path for the file.
        Default will output to the working directory.
        
    Returns
    -------
    dictionaries : single item, list
        item, or list, of the dictionary(ies) loaded from the file(s)
        
    Example
    -------
    exp_info = load_dictionary("exp_01_info", keys=["id", "wire"], directory="exps/")
    """ 

    filenames = args
    file_format = ".json"

    keys_arg = keys
    # if a singular string, add it to an array
    if isinstance(keys, str):
        keys_arg = [keys]
    
    # if single item in filenames
    # and not singluar string, filenames is (likely) a list of filenames
    if len(filenames) == 1 and isinstance(filenames[0], str) == False:
        logger.debug("Filenames type: %s", type(filenames))
        filenames = filenames[0]
    
    dictionaries = []
    
    # iterate through filenames and load
    for filename in filenames:
        logger.info("Reading file: %s", filename)
        filename = prepare_filename(filename, file_format, directory)
        
        dictionary = json.load(open(filename))
        
        # keys to read in
        if keys_arg != []:
            keys_arg, data = load_data(filename, keys=keys_arg)
            dictionary = create_dictionary(keys_arg, data)
        
        dictionaries.append(dictionary)
    
    # if single key loaded, remove outter container
    if len(dictionaries) == 1:
        dictionaries = dictionaries[0]
    
    return dictionaries

def load_data(*args, file_format=".json", keys=[], directory=""):
    """
    Load a item(s) from a file, or multiple files.
    
    Note: currently only deals with .json files.
    
    Parameters
    ----------
    *args : str, multiple str, list of str, array of str etc.
        A string, multiple strings, or collection of strings with the 
        filename(s).

    file_format = : ".json", str, optional
        The file formart / extension.
    keys : [], list, array, str, optional
        Names of items to load from the file(s).
        Default will load all items from the file(s).
        Can provide a single string to load a single key.
    directory : "", str, optional
        The path for the file.
        Default will output to the working directory.
        
    Returns
    -------
    data : single item, list
        item, or list, of the data loaded from the file(s)
    keys : single item, list 
        item, or list, of the key(s) loaded from the file(s)
        
    Example
    -------
    power, voltages = load_data("power_output.json")
    power, voltages = load_data("power_output_01", "power_output_02", 
                                    dir="data/20180903")
    power, voltages = load_data(["power_output_01", "power_output_02"],
                                    keys=["1.2, 1.4, 2.2"])
    wire_id, _ = load_data("wire_001", keys = "id")
    """

    filenames = args

    keys_arg = keys
    # if a singular string, add it to an array
    if isinstance(keys, str):
        keys_arg = [keys]

    keys = []
    data = []

    # if single item in filenames
    # and not singluar string, filenames is (likely) a list of filenames
    if len(filenames) == 1 and isinstance(filenames[0], str) == False:
        logger.debug("Filenames type: %s", type(filenames))
        filenames = filenames[0]

    # iterate through filenames and load
    for filename in filenames:
        logger.info("Reading file: %s", filename)
        filename = prepare_filename(filename, file_format, directory)

        keys_in = None
        data_in = None

        if file_format == ".json":
            data_in = json.load(open(filename))

            # sort which keys to read in
            if keys_arg == []:
                # default to read in all keys
                keys_in = data_in.keys()
            else:
                # user given keys
                keys_in = keys_arg

            for key in keys_in:
                keys.append(key)
                data.append(data_in[key])
            
        else: 
            raise Exception(
                    "Only the .json file format is currently supported.")

    # if single key loaded, remove outter container
    if len(data) == 1:
        keys = keys[0]
        data = data[0]

    return keys, data

def load_item(*args, file_format=".json", keys=[], directory=""):
    """
    Load a item(s) from a file, or multiple files.
    Similar to the function load_data(), but this one does not 
    return the keys variable.

    See load_data() for more information.

    Returns
    -------
    item
        The data loaded from the file(s).

    Example
    -------
    id = load_item("experiment_id")
    weights = load_item("system_01", "system_02", keys = "weights")

    """
    key, item = load_data(args, file_format=file_format, 
                          keys=keys, directory=directory)
    
    return item

def save_data(*args, file_format=".json", directory=""):
    """
    Save a variable(s) to a file(s).
    
    Note: currently only deals with .json files.
    
    Parameters
    ----------
    *args : str, data
        Given as a pair, a string for the filename and the data to save.
        Multiple pairs can be inputted.

    file_format = : ".json", str, optional
        The file formart / extension.
    directory : ".", str, optional
        The path for the file, which will be created if it does not exist.
        Default will output to the working directory.
        
    Example
    -------
    save_data("wire_001", wire, dir="data/20180903")
    save_data("power_output_01", output_01,
                "power_output_02", output_02)
    """
    
    check_argument_pairs(args)

    # if the directory does not exist, create it
    if directory != "" and os.path.exists(directory) == False:
        logger.info("Creating directory: %s", directory)
        os.makedirs(directory)

    # create name and data pairs
    pairs = process_arguement_pairs(args)

    # iterate through pairs and output
    for pair in pairs:
        filename = pair[0]
        data = pair[1]
        
        filename = prepare_filename(filename, file_format, directory)
        logger.info("Saving file: %s", filename)
        
        if file_format == ".json":
            # if data is not a dictionary already, create a dictionary
            if isinstance(data, dict) == False:
                data = create_dictionary("d", data)
            
            # convert dictionary items for writing to a json file
            prepare_json_dictionary(data)

            # output json file
            with open(filename,'w') as file :
                json.dump(data, file)

        else: 
            raise Exception(
                    "Only the .json file format is currently supported.")
    
    return 0
# Import packages.
import os


# A function to create an output folder.
def make_output_folder(script_directory):

    output_directory = script_directory + '\\Output'

    os.makedirs(output_directory)
    
    return output_directory
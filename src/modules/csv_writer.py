import csv
from datetime import datetime
import os


def write_csv(arr, product, file_path):
    """
    Writes a CSV file with a specific naming convention and stores it at the specified file path.

    Parameters:
    - arr (list): List of dictionaries representing the data to be written to the CSV.
    - product (str): The product entered by the user.
    - file_path (str): The path where the CSV needs to be stored.

    Returns:
    - str: The file name of the created CSV file.
    """

    # Change the current working directory to the specified file path
    os.chdir(file_path)

    # Get the keys (column names) from the first dictionary in the list
    keys = arr[0].keys()
    now = datetime.now()

    # Construct the file name with the specified naming convention
    file_name = product + now.strftime("%m%d%y_%H%M") + '.csv'
    a_file = open(file_name, "w", newline='')
    dict_writer = csv.DictWriter(a_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(arr)
    a_file.close()
    return file_name

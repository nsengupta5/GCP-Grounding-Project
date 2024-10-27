"""
File: helper.py
Author: Nikhil Sengupta
Created On: 25-10-2024
Last Updated On: 27-10-2024
Email: nikhil.sengupta10@proton.me

Description: This script contains helper functions for working with Terraform files.
"""

import hcl2


def get_tfvars(file_path: str) -> dict:
    """
    Reads a Terraform variables file and returns its contents as a dictionary.

    Args:
        file_path (str): The path to the Terraform variables file.

    Returns:
        dict: The contents of the Terraform variables file.
    """
    with open(file_path, "r") as tfvars_fp:
        tfvars = hcl2.load(tfvars_fp)
    return tfvars

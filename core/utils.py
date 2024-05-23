"""
Utils functions
"""

from uuid import UUID
import re


# Define a function for validating an Email
def check_email(email):
    regex = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )
    if re.fullmatch(regex, email):
        return True
    else:
        return False


# Check if a value is a valid UUID
def is_valid_uuid(value):
    try:
        UUID(value, version=4)
        return True
    except ValueError:
        return False

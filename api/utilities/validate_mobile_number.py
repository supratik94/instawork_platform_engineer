__author__ = "Supratik Majumdar"
__status__ = "Development"

import re


def validate_mobile_number(mobile_number: str):
    if re.match(r"^[0-9]*$", mobile_number) is None:
        raise ValueError("mobile number format is invalid")

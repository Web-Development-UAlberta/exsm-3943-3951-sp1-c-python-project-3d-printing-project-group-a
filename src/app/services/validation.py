import re

VALID_PROVINCES = [
    "AB", "BC", "MB", "NB", "NL",
    "NS", "NT", "NU", "ON", "PE",
    "QC", "SK", "YT"
]

def validate_postal_code(postal_code):
    # Canadian postal code format: A1A 1A1 or A1A1A1
    pattern = r'^[A-Za-z]\d[A-Za-z][\s]?\d[A-Za-z]\d$'
    if not re.match(pattern, postal_code):
        return False, "Invalid postal code format (e.g. T5A 0A1)"
    return True, None


def validate_province(province):
    if province.upper() not in VALID_PROVINCES:
        return False, f"Invalid province code. Must be one of: {', '.join(VALID_PROVINCES)}"
    return True, None


def validate_phone(phone_number):
    # accepts formats: 780-555-0101, 7805550101, (780) 555-0101
    pattern = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4}$'
    if not re.match(pattern, phone_number):
        return False, "Invalid phone number format (e.g. 780-555-0101)"
    return True, None
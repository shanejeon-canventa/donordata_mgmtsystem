from datetime import datetime
from typing import Optional, List


def parse_date_string(date_string: str) -> list:
    """Splits a full timestamp string into separate date and time objects."""
    full_datetime = datetime.strptime(date_string, "%m/%d/%Y %I:%M %p")
    return [full_datetime.date(), full_datetime.time()]


def _parse_csv_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parses raw MM/DD/YYYY strings into datetime objects. Returns None on empty fields."""
    if not date_str:
        return None
        
    clean_val = date_str.strip()
    if not clean_val:
        return None
        
    try:
        return datetime.strptime(clean_val, '%m/%d/%Y')
    except ValueError:
        # Invalid or non-standard date format encountered in CSV row
        return None


def _parse_csv_bool(bool_str: Optional[str]) -> bool:
    """Normalizes typical text indicators (Y/N, Positive/Negative) into standard booleans."""
    if not bool_str:
        return False
        
    clean_val = bool_str.strip().lower()
    
    # Check negative indicators first
    if clean_val in ('n', 'negative', 'not detected', '') or clean_val.startswith('neg'):
        return False
    # Check positive indicators
    if clean_val in ('y', 'positive', 'detected') or clean_val.startswith('pos'):
        return True
        
    raise ValueError(f"Unrecognized boolean value in CSV: '{bool_str}'")


def _parse_csv_float(float_str: Optional[str]) -> float:
    """Safely coerces numeric strings to floats, defaulting to 0.0 for missing data."""
    if not float_str:
        return 0.0
        
    clean_val = float_str.strip()
    if not clean_val:
        return 0.0
        
    try:
        return float(clean_val)
    except ValueError:
        return 0.0


def _parse_csv_list(list_str: Optional[str]) -> List[str]:
    """Splits delimited text into a cleaned list, handling both commas and semicolons."""
    if not list_str:
        return []
        
    clean_val = list_str.strip()
    if not clean_val:
        return []
        
    delimiter = ';' if ';' in clean_val else ','
    return [item.strip() for item in clean_val.split(delimiter) if item.strip()]
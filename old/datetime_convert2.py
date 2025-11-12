from datetime import datetime
from typing import Optional, Tuple

def detect_datetime_format(date_string: str) -> Tuple[Optional[datetime], Optional[str]]:
    """
    Automatically detect the format of a date string and return both the datetime object
    and the format type.
    
    Args:
        date_string: The date string to parse
        
    Returns:
        A tuple of (datetime object, format name) if parsing succeeds, (None, None) otherwise
    """
    # Clean the string
    date_string = date_string.strip()
    
    # Check if it's a Unix timestamp (all digits, 10 or 13 digits)
    if date_string.isdigit():
        try:
            timestamp = int(date_string)
            # Handle both seconds (10 digits) and milliseconds (13 digits)
            if len(date_string) == 13:
                dt = datetime.fromtimestamp(timestamp / 1000)
                return dt, "Unix timestamp (milliseconds)"
            elif len(date_string) == 10:
                dt = datetime.fromtimestamp(timestamp)
                return dt, "Unix timestamp (seconds)"
        except (ValueError, OSError):
            pass
    
    # Dictionary mapping format strings to human-readable names
    format_types = {
        # ISO 8601 formats with timezone
        "%Y-%m-%dT%H:%M:%S%z": "ISO 8601 (with timezone)",
        "%Y-%m-%dT%H:%M:%S.%f%z": "ISO 8601 (with microseconds and timezone)",
        "%Y-%m-%d %H:%M:%S%z": "ISO 8601 (datetime with timezone)",
        "%Y-%m-%d %H:%M:%S.%f%z": "ISO 8601 (datetime with microseconds and timezone)",
        
        # ISO 8601 formats
        "%Y-%m-%d %H:%M:%S": "ISO 8601 (datetime)",
        "%Y-%m-%dT%H:%M:%S": "ISO 8601 (T-separated)",
        "%Y-%m-%dT%H:%M:%S.%f": "ISO 8601 (with microseconds)",
        "%Y-%m-%dT%H:%M:%SZ": "ISO 8601 (UTC/Zulu)",
        "%Y-%m-%dT%H:%M:%S.%fZ": "ISO 8601 (UTC with microseconds)",
        "%Y-%m-%d": "ISO 8601 (date only)",
        
        # US formats
        "%m/%d/%Y": "US format (MM/DD/YYYY)",
        "%m/%d/%Y %H:%M:%S": "US format (MM/DD/YYYY with time)",
        "%m/%d/%y": "US format (MM/DD/YY)",
        "%m-%d-%Y": "US format (MM-DD-YYYY)",
        
        # European formats
        "%d/%m/%Y": "European format (DD/MM/YYYY)",
        "%d/%m/%Y %H:%M:%S": "European format (DD/MM/YYYY with time)",
        "%d-%m-%Y": "European format (DD-MM-YYYY)",
        "%d.%m.%Y": "European format (DD.MM.YYYY)",
        
        # Text month formats
        "%B %d, %Y": "Long month format (Month DD, YYYY)",
        "%b %d, %Y": "Short month format (Mon DD, YYYY)",
        "%d %B %Y": "European text format (DD Month YYYY)",
        "%d %b %Y": "European text format (DD Mon YYYY)",
        
        # Other common formats
        "%Y/%m/%d": "Asian format (YYYY/MM/DD)",
        "%Y/%m/%d %H:%M:%S": "Asian format (YYYY/MM/DD with time)",
        "%d-%b-%Y": "Short month format (DD-Mon-YYYY)",
        "%Y%m%d": "Compact format (YYYYMMDD)",
    }
    
    # Try each format
    for fmt, format_name in format_types.items():
        try:
            dt = datetime.strptime(date_string, fmt)
            return dt, format_name
        except ValueError:
            continue
    
    # If none of the formats work, return None, None
    return None, None


def parse_datetime(date_string: str) -> Optional[datetime]:
    """
    Automatically detect the format of a date string and convert it to a datetime object.
    
    Args:
        date_string: The date string to parse
        
    Returns:
        A datetime object if parsing succeeds, None otherwise
    """
    dt, _ = detect_datetime_format(date_string)
    if dt is None:
        print(f"Could not parse date string: '{date_string}'")
    return dt


def print_datetime_format(date_string: str) -> None:
    """
    Detect and print the format type of a date string.
    
    Args:
        date_string: The date string to analyze
    """
    dt, format_name = detect_datetime_format(date_string)
    
    if dt and format_name:
        print(f"'{date_string}' -> {format_name}")
        print(f"  Parsed as: {dt}")
    else:
        print(f"'{date_string}' -> Unknown format (could not parse)")
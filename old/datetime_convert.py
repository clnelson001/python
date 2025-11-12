from datetime import datetime
from typing import Optional

def parse_datetime(date_string: str) -> Optional[datetime]:
    """
    Automatically detect the format of a date string and convert it to a datetime object.
    
    Args:
        date_string: The date string to parse
        
    Returns:
        A datetime object if parsing succeeds, None otherwise
    """
    # Common date formats to try
    formats = [
        # ISO 8601 formats
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%d",
        
        # US formats
        "%m/%d/%Y",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%y",
        "%m-%d-%Y",
        
        # European formats
        "%d/%m/%Y",
        "%d/%m/%Y %H:%M:%S",
        "%d-%m-%Y",
        "%d.%m.%Y",
        
        # Text month formats
        "%B %d, %Y",  # January 01, 2024
        "%b %d, %Y",  # Jan 01, 2024
        "%d %B %Y",   # 01 January 2024
        "%d %b %Y",   # 01 Jan 2024
        
        # Other common formats
        "%Y/%m/%d",
        "%Y/%m/%d %H:%M:%S",
        "%d-%b-%Y",   # 01-Jan-2024
        "%Y%m%d",     # 20240101
    ]
    
    # Clean the string
    date_string = date_string.strip()
    
    # Try each format
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    # If none of the formats work, return None
    print(f"Could not parse date string: '{date_string}'")
    return None


# Example usage
if __name__ == "__main__":
    test_dates = [
        "2024-03-15",
        "03/15/2024",
        "15/03/2024",
        "2024-03-15 14:30:00",
        "March 15, 2024",
        "15 Mar 2024",
        "2024/03/15",
    ]
    
    for date_str in test_dates:
        result = parse_datetime(date_str)
        print(f"{date_str:30} -> {result}")
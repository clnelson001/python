"""
Datetime Conversion Utility
Automatically detect, parse, convert, and format datetime strings in various formats.
"""

from datetime import datetime, timezone
from typing import Optional, Tuple, List
import sys

def list_func():
    funcStr ="""
    # detect_datetime_format(date_string: str) -> Tuple[Optional[datetime], Optional[str]]
    # parse_datetime(date_string: str) -> Optional[datetime]
    # print_datetime_format(date_string: str) -> None
    # datetime_to_string(dt: datetime, format_type: str) -> str
    # sort_datetimes(date_strings: List[str], make_aware: bool = True) -> List[Tuple[datetime, str, str]]
    """
    print("\n")
    print("-" * 70)
    print("Available Functions:")
    print(funcStr)
    print("-" * 70)

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


def datetime_to_string(dt: datetime, format_type: str) -> str:
    """
    Convert a datetime object back to a string in the specified format.
    
    Args:
        dt: The datetime object to convert
        format_type: The format type (e.g., "ISO 8601 (UTC/Zulu)", "Unix timestamp (seconds)", etc.)
        
    Returns:
        A formatted string representation of the datetime
    """
    format_map = {
        # Unix timestamps
        "Unix timestamp (seconds)": lambda d: str(int(d.timestamp())),
        "Unix timestamp (milliseconds)": lambda d: str(int(d.timestamp() * 1000)),
        
        # ISO 8601 formats with timezone
        "ISO 8601 (with timezone)": lambda d: d.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "ISO 8601 (with microseconds and timezone)": lambda d: d.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "ISO 8601 (datetime with timezone)": lambda d: d.strftime("%Y-%m-%d %H:%M:%S%z"),
        "ISO 8601 (datetime with microseconds and timezone)": lambda d: d.strftime("%Y-%m-%d %H:%M:%S.%f%z"),
        
        # ISO 8601 formats
        "ISO 8601 (datetime)": lambda d: d.strftime("%Y-%m-%d %H:%M:%S"),
        "ISO 8601 (T-separated)": lambda d: d.strftime("%Y-%m-%dT%H:%M:%S"),
        "ISO 8601 (with microseconds)": lambda d: d.strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "ISO 8601 (UTC/Zulu)": lambda d: d.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ISO 8601 (UTC with microseconds)": lambda d: d.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "ISO 8601 (date only)": lambda d: d.strftime("%Y-%m-%d"),
        
        # US formats
        "US format (MM/DD/YYYY)": lambda d: d.strftime("%m/%d/%Y"),
        "US format (MM/DD/YYYY with time)": lambda d: d.strftime("%m/%d/%Y %H:%M:%S"),
        "US format (MM/DD/YY)": lambda d: d.strftime("%m/%d/%y"),
        "US format (MM-DD-YYYY)": lambda d: d.strftime("%m-%d-%Y"),
        
        # European formats
        "European format (DD/MM/YYYY)": lambda d: d.strftime("%d/%m/%Y"),
        "European format (DD/MM/YYYY with time)": lambda d: d.strftime("%d/%m/%Y %H:%M:%S"),
        "European format (DD-MM-YYYY)": lambda d: d.strftime("%d-%m-%Y"),
        "European format (DD.MM.YYYY)": lambda d: d.strftime("%d.%m.%Y"),
        
        # Text month formats
        "Long month format (Month DD, YYYY)": lambda d: d.strftime("%B %d, %Y"),
        "Short month format (Mon DD, YYYY)": lambda d: d.strftime("%b %d, %Y"),
        "European text format (DD Month YYYY)": lambda d: d.strftime("%d %B %Y"),
        "European text format (DD Mon YYYY)": lambda d: d.strftime("%d %b %Y"),
        
        # Other common formats
        "Asian format (YYYY/MM/DD)": lambda d: d.strftime("%Y/%m/%d"),
        "Asian format (YYYY/MM/DD with time)": lambda d: d.strftime("%Y/%m/%d %H:%M:%S"),
        "Short month format (DD-Mon-YYYY)": lambda d: d.strftime("%d-%b-%Y"),
        "Compact format (YYYYMMDD)": lambda d: d.strftime("%Y%m%d"),
    }
    
    if format_type in format_map:
        return format_map[format_type](dt)
    else:
        # Default to ISO 8601 if format type not recognized
        return dt.isoformat()


def sort_datetimes(date_strings: List[str], make_aware: bool = True) -> List[Tuple[datetime, str, str]]:
    """
    Parse, sort, and return datetime strings with their format information.
    
    Args:
        date_strings: List of date strings to parse and sort
        make_aware: If True, make all datetimes timezone-aware (UTC) for proper sorting
        
    Returns:
        List of tuples: (datetime_object, format_type, original_string) sorted chronologically
    """
    parsed_data = []
    
    for date_str in date_strings:
        dt, format_type = detect_datetime_format(date_str)
        if dt:
            # Make timezone-aware for proper sorting if requested
            if make_aware and dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            parsed_data.append((dt, format_type, date_str))
        else:
            print(f"Warning: Could not parse '{date_str}'")
    
    # Sort by datetime
    parsed_data.sort(key=lambda x: x[0])
    
    return parsed_data


# Example usage and tests
if __name__ == "__main__":
    if len(sys.argv) == 2:
        list_func()
        sys.exit(0)
    print("=" * 70)
    print("DateTime Conversion Utility - Examples")
    print("=" * 70)
    
    # Test various date formats
    test_dates = [
        "2025-11-12T10:03:00Z",
        "2025-11-11 05:03:00-0500",
        "1731405780",
        "03/15/2024",
        "15/03/2024",
        "March 15, 2024",
        "2024-03-15",
    ]
    
    print("\n1. Detecting formats:")
    print("-" * 70)
    for date_str in test_dates:
        print_datetime_format(date_str)
        print()
    
    print("\n2. Parsing and converting back:")
    print("-" * 70)
    for date_str in test_dates[:3]:
        dt, fmt = detect_datetime_format(date_str)
        if dt and fmt:
            converted = datetime_to_string(dt, fmt)
            print(f"Original:  {date_str}")
            print(f"Format:    {fmt}")
            print(f"Converted: {converted}")
            print()
    
    print("\n3. Sorting mixed format dates:")
    print("-" * 70)
    times_to_sort = [
        "2025-11-12T10:03:00Z",
        "2025-11-11 05:03:00-0500",
        "1731405780",
    ]
    
    sorted_data = sort_datetimes(times_to_sort)
    
    print("Sorted chronologically:")
    for dt, fmt, original in sorted_data:
        utc_time = dt.astimezone(timezone.utc)
        print(f"{original:30} -> {utc_time} UTC")
    
    print("\n4. Convert back to original formats after sorting:")
    print("-" * 70)
    for dt, fmt, original in sorted_data:
        converted = datetime_to_string(dt, fmt)
        print(f"{converted:30} ({fmt})")
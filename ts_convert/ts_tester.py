#from datetime_convert2 import parse_datetime,detect_datetime_format
from datetime import timezone
import ts_convert
    # detect_datetime_format(date_string: str) -> Tuple[Optional[datetime], Optional[str]]:
    # parse_datetime(date_string: str) -> Optional[datetime]:
    # print_datetime_format(date_string: str) -> None:
    # datetime_to_string(dt: datetime, format_type: str) -> str:
    # sort_datetimes(date_strings: List[str], make_aware: bool = True) -> List[Tuple[datetime, str, str]]:

# print(t_type)
times = [
    "2025-11-12T10:03:00Z",
    "2025-11-11 05:03:00-0500",
    "1731405780",
    "1762979494"
]

parsed_times = []
for t in times:
   # dt = parse_datetime(t)
    dt,fmt = ts_convert.detect_datetime_format(t)
    print(fmt)
    if dt:
        # If naive (no timezone), assume it's UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        parsed_times.append(dt)

# Now you can sort
sorted_times = sorted(parsed_times)

for dt in sorted_times:
    print(dt)
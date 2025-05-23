from consts.enum import Location, LocationStr
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from consts.scheduler import scheduler


def clean_dict(data: dict[str, str]) -> dict[str, str]:
    """
    Remove None or empty string values from a dictionary and strip whitespace from string values.
    """
    cleaned_data = {}
    for k, v in data.items():
        if v is None or v == "":
            continue
        if isinstance(v, str):
            cleaned_data[k] = v.strip()
        else:
            cleaned_data[k] = v
    return cleaned_data


def get_location_id(location_str: str) -> Location:
    try:
        location_enum = LocationStr(location_str)
        return Location[location_enum.name]
    except ValueError:
        raise ValueError(f"Invalid location string: {location_str}")


def get_sleep_seconds() -> int:
    chile_tz = ZoneInfo("America/Santiago")
    now = datetime.now(chile_tz)
    day = now.isoweekday()
    start_str, end_str = scheduler[day]
    sh, sm = map(int, start_str.split(":"))
    eh, em = map(int, end_str.split(":"))

    start = now.replace(hour=sh, minute=sm, second=0, microsecond=0)
    end = now.replace(hour=eh, minute=em, second=0, microsecond=0)

    if start <= now <= end:
        return 0
    elif now < start:
        return (start - now).total_seconds()
    else:
        next_day = (day % 7) + 1
        nsh, nsm = map(int, scheduler[next_day][0].split(":"))
        next_start = (now + timedelta(days=1)).replace(
            hour=nsh, minute=nsm, second=0, microsecond=0
        )
        return (next_start - now).total_seconds()

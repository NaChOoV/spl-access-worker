from consts.enum import Location, LocationStr


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

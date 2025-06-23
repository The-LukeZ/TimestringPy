# -*- coding: utf-8 -*-

"""
Timestring Parser (Py)
~~~~~~~~~~~~~~~~

This script provides functionality to parse human-readable timestrings
into floating numbers. It supports various time units and allows
customization through options.

It is originally taken from the npm-module ["timestring"](https://www.npmjs.com/package/timestring) (javascript)
but converted into Python.
"""

__all__ = ["parse_timestring", "DEFAULT_OPTS", "DEFAULT_UNIT_MAP"]

import re
from typing import Dict, Iterator, List, Match, Optional, Union

DEFAULT_OPTS: Dict[str, Union[int, float]] = {
    "hoursPerDay": 24,
    "daysPerWeek": 7,
    "weeksPerMonth": 4,
    "monthsPerYear": 12,
    "daysPerYear": 365.25
}

DEFAULT_UNIT_MAP: Dict[str, List[str]] = {
    "ms":   ["ms", "milli", "millisecond", "milliseconds"],
    "s":    ["s", "sec", "secs", "second", "seconds"],
    "m":    ["m", "min", "mins", "minute", "minutes"],
    "h":    ["h", "hr", "hrs", "hour", "hours"],
    "d":    ["d", "day", "days"],
    "w":    ["w", "week", "weeks"],
    "mth":  ["mon", "mth", "mths", "month", "months"],
    "y":    ["y", "yr", "yrs", "year", "years"]
}


def parse_timestring(
    value: Union[str, int],
    return_unit: Optional[str] = None,
    opts: Dict[str, Union[int, float]] = DEFAULT_OPTS,
    unit_map: Dict[str, List[str]] = DEFAULT_UNIT_MAP
) -> Union[int, float]:
    """
    Parses a timestring into a floating number.

    ### Args:
        value (str | int): The timestring to parse (e.g., "1h2m3s", "5 days", etc.) OR the seconds but then it needs to be of type `int`.
        return_unit (str, optional): The time unit that is returned. A key or a value of the unit_map (param) or DEFAULT_UNIT_MAP.
            Defaults to None, which results in seconds being returned.
        opts (dict, optional): Optional dictionary with custom options. Defaults to DEFAULT_OPTS.

            `hoursPerDay` (int): The number of hours in a day (defaults to 24).
            `daysPerWeek` (int): The number of days in a week (defaults to 7).
            `weeksPerMonth` (int): The number of weeks in a month (defaults to 4).
            `monthsPerYear` (int): The number of months in a year (defaults to 12).
            `daysPerYear` (float): The average number of days in a year (defaults to 365.25).

        units (dict, optional): Optional dictionary with custom units (e.g. for another language). Defaults to DEFAULT_OPTS.

            `ms` ( list[str] ): All strings that should be considered a unit of "milliseconds".
            `s` ( list[str] ): All strings that should be considered a unit of "seconds".
            `m` ( list[str] ): All strings that should be considered a unit of "minutes".
            `h` ( list[str] ): All strings that should be considered a unit of "hours".
            `d` ( list[str] ): All strings that should be considered a unit of "days".
            `w` ( list[str] ): All strings that should be considered a unit of "weeks".
            `mth` ( list[str] ): All strings that should be considered a unit of "months".
            `y` ( list[str] ): All strings that should be considered a unit of "years".

    ### Returns:
        float: The parsed time in seconds or the return unit, if given.

    ### Raises:
        ValueError: If the value cannot be parsed.
    """

    if isinstance(value, int) or (isinstance(value, str) and value.isnumeric()):
        value = str(value) + "s"

    matches: List[Match[str]] = list(re.finditer(r'[-+]?[0-9.]+[a-z]+',
                                                 re.sub(r'[^.\w+-]+', "", value.lower())))

    if not matches:
        raise ValueError(f"Failed to parse value: `{value}`")

    UNIT_VALUES: Dict[str, float] = _get_unit_values(opts)
    UNIT_MAP: Dict[str, List[str]] = _get_unit_map(unit_map)
    total_seconds: float = 0
    for match in matches:
        val: Optional[Match[str]] = re.search(r'[-+]?[0-9.]+', match.group(0))
        unit: Optional[Match[str]] = re.search(r'[a-z]+', match.group(0))
        if val is None or unit is None:
            raise ValueError(f"Failed to parse match: `{match.group(0)}`")
        total_seconds += _get_seconds(float(val.group(0)),
                                      unit.group(0), UNIT_VALUES, UNIT_MAP)

    if return_unit:
        return _convert(total_seconds, return_unit, UNIT_VALUES, UNIT_MAP)

    return total_seconds


def _get_unit_values(opts: Dict[str, Union[int, float]]) -> Dict[str, float]:
    """
    Calculates conversion factors based on options.

    Args:
        opts (dict): Dictionary with options (same as parse_timestring).

    Returns:
        dict: Dictionary with conversion factors for each unit.
    """

    unit_values: Dict[str, float] = {
        "ms": 0.001,
        "s": 1,
        "m": 60,
        "h": 3600
    }
    _opts: Dict[str, Union[int, float]] = DEFAULT_OPTS.copy()
    _opts.update(opts)

    unit_values["d"] = _opts["hoursPerDay"] * unit_values["h"]
    unit_values["w"] = _opts["daysPerWeek"] * unit_values["d"]
    unit_values["mth"] = (_opts["daysPerYear"] /
                          _opts["monthsPerYear"]) * unit_values["d"]
    unit_values["y"] = _opts["daysPerYear"] * unit_values["d"]

    return unit_values


def _get_seconds(value: float, unit: str, unit_values: Dict[str, float], unit_map: Dict[str, List[str]]) -> float:
    """
    Converts a value to seconds based on the given unit.

    Args:
        value (float): The value to convert.
        unit (str): The unit of the value.
        unit_values (dict): Dictionary with conversion factors.

    Returns:
        float: The value in seconds.
    """
    return value * unit_values[_get_unit_key(unit, unit_map)]


def _get_unit_key(unit: str, unit_map: Dict[str, List[str]]) -> str:
    """
    Finds the key in the unit_map that corresponds to the given unit.

    Args:
        unit (str): The unit to search for.

    Returns:
        str: The key in UNIT_MAP, if found.

    Raises:
        ValueError: If the unit is not supported.
    """
    for key in unit_map.keys():
        if unit in unit_map[key]:
            return key
    raise ValueError(f"The unit '{unit}' is not supported by timestring")


def _get_unit_map(unit_map: Dict[str, List[str]]) -> Dict[str, List[str]]:
    _um: Dict[str, List[str]] = {}
    # Create a deep copy of DEFAULT_UNIT_MAP to avoid modifying the original
    for key, value in DEFAULT_UNIT_MAP.items():
        _um[key] = value.copy()

    # Only update if unit_map is different from DEFAULT_UNIT_MAP
    if unit_map is not DEFAULT_UNIT_MAP:
        _um.update(unit_map)
    return _um


def _convert(value: float, unit: str, unit_values: Dict[str, float], unit_map: Dict[str, List[str]]) -> float:
    return (value / unit_values[_get_unit_key(unit, unit_map)])

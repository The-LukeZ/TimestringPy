# -*- coding: utf-8 -*-

"""
Timestring Parser (Py)
~~~~~~~~~~~~~~~~

This script provides functionality to parse human-readable timestrings
into timedelta objects. It supports various time units and allows
customization through options.

It is originally taken from the npm-module ["timestring"](https://www.npmjs.com/package/timestring) (javascript)
but it's now converted into Python.
"""

__title__ = 'TimestringPy'
__author__ = 'The-LukeZ'
__license__ = 'MIT'
__copyright__ = 'Copyright (C) 2024 The-LukeZ'
__version__ = '1.0'
__credits__ = ["mike182uk"]
__all__ = ["parse_timestring", "DEFAULT_OPTS", "UNIT_MAP"]

import re
from datetime import timedelta

DEFAULT_OPTS = {
    "hoursPerDay": 24,
    "daysPerWeek": 7,
    "weeksPerMonth": 4,
    "monthsPerYear": 12,
    "daysPerYear": 365.25
}

UNIT_MAP = {
    "ms":   ["ms", "milli", "millisecond", "milliseconds"],
    "s":    ["s", "sec", "secs", "second", "seconds"],
    "m":    ["m", "min", "mins", "minute", "minutes"],
    "h":    ["h", "hr", "hrs", "hour", "hours"],
    "d":    ["d", "day", "days"],
    "w":    ["w", "week", "weeks"],
    "mth":  ["mon", "mth", "mths", "month", "months"],
    "y":    ["y", "yr", "yrs", "year", "years"]
}

def parse_timestring(value: str | int, opts: dict[str, float] = DEFAULT_OPTS) -> timedelta:
    """
    Parses a timestring into a timedelta object.

    ### Args:
        value (str | int): The timestring to parse (e.g., "1h2m3s", "5 days", etc.) OR the seconds but then it needs to be of type `int`.
        opts (dict, optional): Optional dictionary with custom options. Defaults to DEFAULT_OPTS.

            `hoursPerDay` (int, optional): The number of hours in a day (defaults to 24).
            `daysPerWeek` (int, optional): The number of days in a week (defaults to 7).
            `weeksPerMonth` (int, optional): The number of weeks in a month (defaults to 4).
            `monthsPerYear` (int, optional): The number of months in a year (defaults to 12).
            `daysPerYear` (float, optional): The average number of days in a year (defaults to 365.25).

            If you pass this attribute, ALL keys listed above MUST be given!

    ### Returns:
        timedelta: The parsed time as a timedelta object.

    ### Raises:
        ValueError: If the value cannot be parsed or the return unit is invalid.
    """

    if value.isnumeric() or isinstance(value, int):
        value = value + "s"

    UNIT_VALUES = _get_unit_values(opts)
    matches = re.finditer(r'[-+]?[0-9.]+[a-z]+', re.sub(r'[^.\w+-]+', "", value.lower()))

    if not matches:
        raise ValueError(f"Failed to parse value: `{value}`")

    total_seconds = 0
    for match in matches:
        print(match)
        val, unit = re.search(r'[0-9.]+', match.group(0)), re.search(r'[a-z]+', match.group(0))
        total_seconds += _get_seconds(int(val.group(0)), unit.group(0), UNIT_VALUES)

    return timedelta(seconds=total_seconds)

def _get_unit_values(opts) -> dict[str, float]:
    """
    Calculates conversion factors based on options.

    Args:
        opts (dict): Dictionary with options (same as parse_timestring).

    Returns:
        dict: Dictionary with conversion factors for each unit.
    """

    unit_values = {
        "ms": 0.001,
        "s": 1,
        "m": 60,
        "h": 3600
    }

    unit_values["d"] = opts["hoursPerDay"] * unit_values["h"]
    unit_values["w"] = opts["daysPerWeek"] * unit_values["d"]
    unit_values["mth"] = (opts["daysPerYear"] / opts["monthsPerYear"]) * unit_values["d"]
    unit_values["y"] = opts["daysPerYear"] * unit_values["d"]

    return unit_values

def _get_seconds(value, unit, unit_values) -> float:
    """
    Converts a value to seconds based on the given unit.

    Args:
        value (float): The value to convert.
        unit (str): The unit of the value.
        unit_values (dict): Dictionary with conversion factors.

    Returns:
        float: The value in seconds.
    """
    return value * unit_values[_get_unit_key(unit)]

def _get_unit_key(unit):
    """
    Finds the key in UNIT_MAP that corresponds to the given unit.

    Args:
        unit (str): The unit to search for.

    Returns:
        str: The key in UNIT_MAP or raises an error if not found.

    Raises:
        ValueError: If the unit is not supported.
    """
    for key, aliases in UNIT_MAP.items():
        if unit in aliases:
            return key
    raise ValueError(f"The unit '{unit}' is not supported by timestring")
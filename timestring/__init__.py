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
from datetime import timedelta

DEFAULT_OPTS = {
    "hoursPerDay": 24,
    "daysPerWeek": 7,
    "weeksPerMonth": 4,
    "monthsPerYear": 12,
    "daysPerYear": 365.25
}

DEFAULT_UNIT_MAP = {
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
    value: str | int,
    # I don't know how it can either be a key or one of the values of the DEFAULT_UNIT_MAP - it just works
    return_unit: str | None = None,
    opts: dict[str, int | float] = DEFAULT_OPTS,
    unit_map: dict[str, list[str]] = DEFAULT_UNIT_MAP
) -> int | float:
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

    matches = re.finditer(r'[-+]?[0-9.]+[a-z]+',
                          re.sub(r'[^.\w+-]+', "", value.lower()))

    if not matches:
        raise ValueError(f"Failed to parse value: `{value}`")

    UNIT_VALUES = _get_unit_values(opts)
    UNIT_MAP = _get_unit_map(unit_map)
    total_seconds = 0
    for match in matches:
        val, unit = re.search(r'[0-9.]+', match.group(0)
                              ), re.search(r'[a-z]+', match.group(0))
        if val is None or unit is None:
            raise ValueError(f"Failed to parse match: `{match.group(0)}`")
        total_seconds += _get_seconds(float(val.group(0)),
                                      unit.group(0), UNIT_VALUES, UNIT_MAP)

    if return_unit:
        return _convert(total_seconds, return_unit, UNIT_VALUES, UNIT_MAP)

    return total_seconds


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
    _opts = DEFAULT_OPTS
    _opts.update(opts)

    unit_values["d"] = _opts["hoursPerDay"] * unit_values["h"]
    unit_values["w"] = _opts["daysPerWeek"] * unit_values["d"]
    unit_values["mth"] = (_opts["daysPerYear"] /
                          _opts["monthsPerYear"]) * unit_values["d"]
    unit_values["y"] = _opts["daysPerYear"] * unit_values["d"]

    return unit_values


def _get_seconds(value, unit, unit_values, unit_map) -> float:
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


def _get_unit_key(unit, unit_map):
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


def _get_unit_map(unit_map) -> dict[str, list[str]]:
    _um = DEFAULT_UNIT_MAP
    _um.update(unit_map)
    return _um


def _convert(value, unit, unit_values, unit_map) -> float:
    return (value / unit_values[_get_unit_key(unit, unit_map)])

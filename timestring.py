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
__all__ = ["TimestringPy", "DEFAULT_OPTS", "UNIT_MAP"]

from re import (
    sub as re_sub,
    match as re_match
)
from datetime import timedelta

DEFAULT_OPTS = {
    "hoursPerDay": 24,
    "daysPerWeek": 7,
    "weeksPerMonth": 4,
    "monthsPerYear": 12,
    "daysPerYear": 365.25
}

UNIT_MAP = {
    "ms": ["ms", "milli", "millisecond", "milliseconds"],
    "s": ["s", "sec", "secs", "second", "seconds"],
    "m": ["m", "min", "mins", "minute", "minutes"],
    "h": ["h", "hr", "hrs", "hour", "hours"],
    "d": ["d", "day", "days"],
    "w": ["w", "week", "weeks"],
    "mth": ["mon", "mth", "mths", "month", "months"],
    "y": ["y", "yr", "yrs", "year", "years"]
}

class TimestringPy:
    """Parse a human readable time string into a timedelta object.

    This class provides a static method `parse_timestring` to convert a human-readable
    time string into a :class:`timedelta` object.
    """

    @staticmethod
    def parse_timestring(value: str, return_unit=None, opts=None) -> timedelta:
        """
        Parses a timestring into a timedelta object.

        Args:
            value (str): The timestring to parse (e.g., "1h2m3s", "5 days").
            return_unit (str, optional): The unit to return the result in. Defaults to None (seconds).
                If provided, the parsed time will be converted to the specified unit before creating
                the timedelta object.
            opts (dict, optional): Optional dictionary with custom options. Defaults to None (uses DEFAULT_OPTS).
                - hoursPerDay (int, optional): The number of hours in a day (defaults to 24).
                - daysPerWeek (int, optional): The number of days in a week (defaults to 7).
                - weeksPerMonth (int, optional): The number of weeks in a month (defaults to 4).
                - monthsPerYear (int, optional): The number of months in a year (defaults to 12).
                - daysPerYear (float, optional): The average number of days in a year (defaults to 365.25).

        Returns:
            datetime.timedelta: The parsed time as a timedelta object.

        Raises:
            ValueError: If the value cannot be parsed or the return unit is invalid.
        """

        opts = dict(**DEFAULT_OPTS, **opts or {})

        # Check if value is a number or number string
        if isinstance(value, (int, float)) or re_match(r"^[-+]?[0-9.]+$"):
            value = str(int(value)) + "ms"

        total_seconds = 0
        unit_values = TimestringPy._get_unit_values(opts)
        groups = re_sub(r"[^\w\-+\.]", "", value.lower()).split(r"[-+]?\d+\.?")

        if not groups:
            raise ValueError(f"The value '{value}' could not be parsed as a timestring.")

        for group in groups:
            if not group:
                continue
            value, unit = group.split(maxsplit=1)
            total_seconds += TimestringPy._get_seconds(float(value), unit, unit_values)

        if return_unit:
            return TimestringPy._convert(total_seconds, return_unit, unit_values)

        return timedelta(seconds=total_seconds)

    @staticmethod
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

    @staticmethod
    def _convert(total_seconds, return_unit, unit_values):
        """
        Converts seconds to another unit.

        Args:
            total_seconds (float): The total time in seconds.
            return_unit (str): The unit to convert to.
            unit_values (dict): Dictionary with conversion factors.

        Returns:
            float: The converted value.
        """

        if return_unit not in unit_values:
            raise ValueError(f"Invalid return unit: {return_unit}")
        return total_seconds / unit_values[return_unit]

    @staticmethod
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

    @staticmethod
    def _get_seconds(value, unit, unit_values):
        """
        Converts a value to seconds based on the given unit.

        Args:
            value (float): The value to convert.
            unit (str): The unit of the value.
            unit_values (dict): Dictionary with conversion factors.

        Returns:
            float: The value in seconds.
        """
        return value * unit_values[TimestringPy._get_unit_key(unit)]

    @staticmethod
    def _convert(total_seconds, return_unit, unit_values):
        """
        Converts seconds to another unit.

        Args:
            total_seconds (float): The total time in seconds.
            return_unit (str): The unit to convert to.
            unit_values (dict): Dictionary with conversion factors.

        Returns:
            float: The converted value.
        """

        # Reuse existing error handling from the previous definition
        return total_seconds / unit_values[TimestringPy._get_unit_key(return_unit)]


Timestring = TimestringPy
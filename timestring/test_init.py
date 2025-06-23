"""
Unit tests for the timestring module

Use with `python -m unittest discover` or `python -m unittest timestring.test_init`
"""

import unittest

from timestring import (DEFAULT_OPTS, DEFAULT_UNIT_MAP, _convert, _get_seconds,
                        _get_unit_key, _get_unit_map, _get_unit_values,
                        parse_timestring)


class TestParseTimestring(unittest.TestCase):

    def test_basic_parsing(self):
        """Test basic timestring parsing"""
        self.assertEqual(parse_timestring("1s"), 1)
        self.assertEqual(parse_timestring("1m"), 60)
        self.assertEqual(parse_timestring("1h"), 3600)
        self.assertEqual(parse_timestring("1d"), 86400)

    def test_integer_input(self):
        """Test integer input converts to seconds"""
        self.assertEqual(parse_timestring(60), 60)
        self.assertEqual(parse_timestring("10"), 10)
        self.assertEqual(parse_timestring("60"), 60)

    def test_complex_timestrings(self):
        """Test complex timestring combinations"""
        self.assertEqual(parse_timestring("1h30m"), 5400)  # 3600 + 1800
        self.assertEqual(parse_timestring("2d12h"), 216000)  # 172800 + 43200
        self.assertEqual(parse_timestring("1h2m3s"), 3723)  # 3600 + 120 + 3

    def test_decimal_values(self):
        """Test decimal time values"""
        self.assertEqual(parse_timestring("1.5h"), 5400)
        self.assertEqual(parse_timestring("2.5m"), 150)

    def test_various_unit_formats(self):
        """Test different unit format aliases"""
        self.assertEqual(parse_timestring("1hour"), 3600)
        self.assertEqual(parse_timestring("1minute"), 60)
        self.assertEqual(parse_timestring("1second"), 1)
        self.assertEqual(parse_timestring("1day"), 86400)

    def test_return_unit_conversion(self):
        """Test return_unit parameter"""
        self.assertEqual(parse_timestring("3600s", return_unit="h"), 1)
        self.assertEqual(parse_timestring("60s", return_unit="m"), 1)
        self.assertEqual(parse_timestring("1h", return_unit="minutes"), 60)

    def test_custom_options(self):
        """Test custom options"""
        custom_opts: dict[str, int | float] = {
            "hoursPerDay": 8  # 8-hour workday
        }
        result = parse_timestring("1d", opts=custom_opts)
        self.assertEqual(result, 28800)  # 8 hours * 3600 seconds

    def test_custom_unit_map(self):
        """Test custom unit mappings"""
        custom_units = {"s": ["s", "sekunde"]}
        result = parse_timestring("5sekunde", unit_map=custom_units)
        self.assertEqual(result, 5)

    def test_negative_values(self):
        """Test negative time values"""
        self.assertEqual(parse_timestring("-1h"), -3600)
        self.assertEqual(parse_timestring("-30m"), -1800)

    def test_positive_sign(self):
        """Test explicit positive sign"""
        self.assertEqual(parse_timestring("+1h"), 3600)
        self.assertEqual(parse_timestring("+30m"), 1800)

    def test_zero_value(self):
        """Test zero value input"""
        self.assertEqual(parse_timestring("0"), 0)
        self.assertEqual(parse_timestring("0s"), 0)
        self.assertEqual(parse_timestring("0m"), 0)
        self.assertEqual(parse_timestring("0h"), 0)

    def test_invalid_input_raises_error(self):
        """Test that invalid inputs raise ValueError"""
        with self.assertRaises(ValueError):
            parse_timestring("invalid")
        with self.assertRaises(ValueError):
            parse_timestring("")

    def test_unsupported_unit_raises_error(self):
        """Test that unsupported units raise ValueError"""
        with self.assertRaises(ValueError):
            parse_timestring("1xyz")


class TestHelperFunctions(unittest.TestCase):

    def test_get_unit_values(self):
        """Test _get_unit_values function"""
        values = _get_unit_values({})
        self.assertEqual(values["s"], 1)
        self.assertEqual(values["m"], 60)
        self.assertEqual(values["h"], 3600)
        self.assertEqual(values["d"], 86400)  # 24 * 3600

    def test_get_unit_values_custom_opts(self):
        """Test _get_unit_values with custom options"""
        custom_opts: dict[str, int | float] = {"hoursPerDay": 8}
        values = _get_unit_values(custom_opts)
        self.assertEqual(values["d"], 28800)  # 8 * 3600

    def test_get_unit_key(self):
        """Test _get_unit_key function"""
        self.assertEqual(_get_unit_key("s", DEFAULT_UNIT_MAP), "s")
        self.assertEqual(_get_unit_key("second", DEFAULT_UNIT_MAP), "s")
        self.assertEqual(_get_unit_key("hours", DEFAULT_UNIT_MAP), "h")
        self.assertEqual(_get_unit_key("day", DEFAULT_UNIT_MAP), "d")

    def test_get_unit_key_invalid_unit(self):
        """Test _get_unit_key with invalid unit"""
        with self.assertRaises(ValueError):
            _get_unit_key("invalid", DEFAULT_UNIT_MAP)

    def test_get_unit_map(self):
        """Test _get_unit_map function"""
        result = _get_unit_map({})
        self.assertEqual(result, DEFAULT_UNIT_MAP)

        custom_map = {"test": ["test"]}
        result = _get_unit_map(custom_map)
        self.assertIn("test", result)
        self.assertIn("s", result)  # Should still have defaults

    def test_get_seconds(self):
        """Test _get_seconds function"""
        unit_values = _get_unit_values({})
        result = _get_seconds(1, "h", unit_values, DEFAULT_UNIT_MAP)
        self.assertEqual(result, 3600)

        result = _get_seconds(30, "m", unit_values, DEFAULT_UNIT_MAP)
        self.assertEqual(result, 1800)

    def test_convert(self):
        """Test _convert function"""
        unit_values = _get_unit_values({})
        result = _convert(3600, "h", unit_values, DEFAULT_UNIT_MAP)
        self.assertEqual(result, 1)

        result = _convert(1800, "m", unit_values, DEFAULT_UNIT_MAP)
        self.assertEqual(result, 30)


class TestConstants(unittest.TestCase):

    def test_default_opts(self):
        """Test DEFAULT_OPTS constant"""
        self.assertEqual(DEFAULT_OPTS["hoursPerDay"], 24)
        self.assertEqual(DEFAULT_OPTS["daysPerWeek"], 7)
        self.assertEqual(DEFAULT_OPTS["weeksPerMonth"], 4)
        self.assertEqual(DEFAULT_OPTS["monthsPerYear"], 12)
        self.assertEqual(DEFAULT_OPTS["daysPerYear"], 365.25)

    def test_default_unit_map(self):
        """Test DEFAULT_UNIT_MAP constant"""
        self.assertIn("ms", DEFAULT_UNIT_MAP)
        self.assertIn("s", DEFAULT_UNIT_MAP)
        self.assertIn("m", DEFAULT_UNIT_MAP)
        self.assertIn("h", DEFAULT_UNIT_MAP)
        self.assertIn("d", DEFAULT_UNIT_MAP)
        self.assertIn("w", DEFAULT_UNIT_MAP)
        self.assertIn("mth", DEFAULT_UNIT_MAP)
        self.assertIn("y", DEFAULT_UNIT_MAP)


if __name__ == "__main__":
    unittest.main()

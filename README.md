# TimestringPy
> Parse a human readable time string into seconds or a specified return unit.

Orinigal source code: [npm i timestring](https://www.npmjs.com/package/timestring) (Javascript)

## Installation

```bash
pip install git+https://github.com/The-LukeZ/TimestringPy
```

## Usage

### Overview

```py
import timestring

value = '1h 15m'
time = timestring.parse_timestring(value)

print(time) # will print 4500
```

**By default the returned time value from `timestring` will be a `float`.**

The time string can contain as many time groups as needed:

```py
import timestring

value = '1d 3h 25m 18s'
time = timestring.parse_timestring(value)

print(time) # will print 98718
```

and can be as messy as you like:

```py
import timestring

value = '1 d    3HOurS 25              min         1   8s'
time = timestring.parse_timestring(value)

print(time) # will print 98718
```

### Keywords

`timestring` will parse the following default keywords into time values:

1. `ms, milli, millisecond, milliseconds` - will parse to milliseconds
2. `s, sec, secs, second, seconds` - will parse to seconds
3. `m, min, mins, minute, minutes` - will parse to minutes
4. `h, hr, hrs, hour, hours` - will parse to hours
5. `d, day, days` - will parse to days
6. `w, week, weeks` - will parse to weeks
7. `mon, mth, mths, month, months` - will parse to months
8. `y, yr, yrs, year, years` - will parse to years

Keywords can be used interchangeably:

```py
import timestring

value = '1day 15h 20minutes 15s'
time = timestring.parse_timestring(value)

print(time) # will print 141615
```

### Return Time Value

By default the return time value will be in seconds. This can be changed by passing one of the strings form the default time-units or an element from the `unit_map`-parameter:

1. `ms` - Milliseconds
2. `s` - Seconds
3. `m` - Minutes
4. `h` - Hours
5. `d` - Days
6. `w` - Weeks
7. `mth` - Months
8. `y` - Years

```py
value = '22h 16m'

hours = timestring.parse_timestring(value, 'h')
days = timestring.parse_timestring(value, 'd')
weeks = timestring.parse_timestring(value, 'w')

print(hours) # will print 22.266666666666666
print(days) # will print 0.9277777777777778
print(weeks) # will print 0.13253968253968254
```

### Optional Configuration

A few assumptions are made by default:

1. There are 24 hours per day
2. There are 7 days per week
3. There are 4 weeks per month
4. There are 12 months per year
5. There are 365.25 days per year

These options can be changed by passing an `dict` to the `opts`-parameter.

The following options are configurable:

1. `hoursPerDay`
2. `daysPerWeek`
3. `weeksPerMonth`
4. `monthsPerYear`
5. `daysPerYear`

```py
import timestring

value = '1d'
opts = {
  'hoursPerDay': 1
}

time = timestring.parse_timestring(value, 'h', opts=opts) # 'h' because we want the number of hours

print(time) # will print 1.0
```

In the example above `hoursPerDay` is being set to `1`. When the time string is being parsed, the return value is being specified as hours. Normally `1d` would parse to the number of seconds in one day à `24h` (as by default there are 24 hours in a day) but because `hoursPerDay` has been set to `1`, `1d` will now only parse to the number of seconds in `1` hour (aka `1d` here).

This would be useful for specific application needs.

*Example - Employees of my company work 7.5 hours a day, and only work 5 days a week. In my time tracking app, when they type `1d` i want 7.5 hours to be tracked. When they type `1w` i want 5 days to be tracked etc.*

```py
import timestring

opts = {
  'hoursPerDay': 7.5,
  'daysPerWeek': 5
}

hoursToday = timestring.parse_timestring('1d', 'h', opts)
daysThisWeek = timestring.parse_timestring('1w', 'd', opts)

print(hoursToday) # will print 7.5
print(daysThisWeek) # will print 5.0
```

You can also pass your own time units to make more languages available.

**Example**
> You have the same example as above, but now you want your German users to type '1 Tag' instead of '1 day' (they may not know the wording), but you want the hours of the day and the amount of days they typed in.

```py
value = '1 tag'

units = {
    "d": ["tag", "d", "day", "days"]
}

opts = {
  'hoursPerDay': 7.5,
  'daysPerWeek': 5
}

hoursToday = timestring.parse_timestring(value, 'h', opts, units)
daysThisWeek = timestring.parse_timestring(value, 'd', opts, units)

print(hoursToday) # will print 7.5 (7.5 hours)
print(daysThisWeek) # will print 1.0 (1 day)
```

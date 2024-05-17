# TimestringPy
> Parse a human readable time string into a timedelta object.

## Installation

```bash
pip install TimestringPy
```

## Usage

### Overview

```py
from timestringpy import parse_timestring

str = '1h 15m'
time = parse_timestring(str)

print(time) # will log 4500
```

> **By default the returned time value from `timestring` will be a `timedelta`.**

The time string can contain as many time groups as needed:

```py
from timestringpy import parse_timestring

str = '1d 3h 25m 18s'
time = parse_timestring(str)

console.log(time) // will log 98718
```

and can be as messy as you like:

```py
const timestring = require('timestring')

let str = '1 d    3HOurS 25              min         1   8s'
let time = timestring(str)

console.log(time) // will log 98718
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
const timestring = require('timestring')

let str = '1day 15h 20minutes 15s'
let time = timestring(str)

console.log(time) // will log 141615
```

### Return Time Value

By default the return time value will be in seconds. This can be changed by passing one of the following strings as an argument to `timestring`:

1. `ms` - Milliseconds
2. `s` - Seconds
3. `m` - Minutes
4. `h` - Hours
5. `d` - Days
6. `w` - Weeks
7. `mth` - Months
8. `y` - Years

```py
const timestring = require('timestring')

let str = '22h 16m'

let hours = timestring(str, 'h')
let days = timestring(str, 'd')
let weeks = timestring(str, 'w')

console.log(hours) // will log 22.266666666666666
console.log(days) // will log 0.9277777777777778
console.log(weeks) // will log 0.13253968253968254
```

### Optional Configuration

A few assumptions are made by default:

1. There are 24 hours per day
2. There are 7 days per week
3. There are 4 weeks per month
4. There are 12 months per year
5. There are 365.25 days per year

These options can be changed by passing an options object as an argument to `timestring`.

The following options are configurable:

1. `hoursPerDay`
2. `daysPerWeek`
3. `weeksPerMonth`
4. `monthsPerYear`
5. `daysPerYear`

```py
const timestring = require('timestring')

let str = '1d'
let opts = {
  hoursPerDay: 1
}

let time = timestring(str, 'h', opts)

console.log(time) // will log 1
```

In the example above `hoursPerDay` is being set to `1`. When the time string is being parsed, the return value is being specified as hours. Normally `1d` would parse to `24` hours (as by default there are 24 hours in a day) but because `hoursPerDay` has been set to `1`, `1d` will now only parse to `1` hour.

This would be useful for specific application needs.

*Example - Employees of my company work 7.5 hours a day, and only work 5 days a week. In my time tracking app, when they type `1d` i want 7.5 hours to be tracked. When they type `1w` i want 5 days to be tracked etc.*

```py
const timestring = require('timestring')

let opts = {
  hoursPerDay: 7.5,
  daysPerWeek: 5
}

let hoursToday = timestring('1d', 'h', opts)
let daysThisWeek = timestring('1w', 'd', opts)

console.log(hoursToday) // will log 7.5
console.log(daysThisWeek) // will log 5
```

It is important to note that the `daysPerYear` configuration option will be used to convert a month or year to seconds, so if you are using custom configuration options make sure that you adjust this value to suit if you expect to be parsing timestrings containing months or years.

## Notes

If the string that is passed into `timestring` can not be parsed then an error will be thrown:

```py
const timestring = require('timestring')

let str = 'aaabbbccc'
let time = timestring(str) // will throw an error
```

If a number is passed into `timestring` it will be treated as a string containing milliseconds:

```py
const timestring = require('timestring')

let time = timestring(3000) // 3s
```
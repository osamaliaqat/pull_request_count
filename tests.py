import collections
from typing import List, Dict
from enum import Enum
from datetime import date, datetime, timedelta, timezone
from pprint import pprint
from dataclasses import dataclass
from main import calculate_datetimes_between, Interval


@dataclass
class Example:
    from_date: date
    to_date: date
    interval: Interval
    result: List[datetime]


EXAMPLES: Dict[str, Example] = {
    "empty_hour_interval": Example(date(2021, 5, 20), date(2021, 5, 19), Interval.hour, []),
    "single_day_all_hours": Example(
        date(2021, 5, 20),
        datetime(2021, 5, 20, 23, 0),
        Interval.hour,
        [
            datetime(2021, 5, 20, 0, 0),
            datetime(2021, 5, 20, 1, 0),
            datetime(2021, 5, 20, 2, 0),
            datetime(2021, 5, 20, 3, 0),
            datetime(2021, 5, 20, 4, 0),
            datetime(2021, 5, 20, 5, 0),
            datetime(2021, 5, 20, 6, 0),
            datetime(2021, 5, 20, 7, 0),
            datetime(2021, 5, 20, 8, 0),
            datetime(2021, 5, 20, 9, 0),
            datetime(2021, 5, 20, 10, 0),
            datetime(2021, 5, 20, 11, 0),
            datetime(2021, 5, 20, 12, 0),
            datetime(2021, 5, 20, 13, 0),
            datetime(2021, 5, 20, 14, 0),
            datetime(2021, 5, 20, 15, 0),
            datetime(2021, 5, 20, 16, 0),
            datetime(2021, 5, 20, 17, 0),
            datetime(2021, 5, 20, 18, 0),
            datetime(2021, 5, 20, 19, 0),
            datetime(2021, 5, 20, 20, 0),
            datetime(2021, 5, 20, 21, 0),
            datetime(2021, 5, 20, 22, 0),
            datetime(2021, 5, 20, 23, 0),
        ],
    ),
    "single_week_all_days": Example(
        date(2021, 5, 17),
        date(2021, 5, 23),
        Interval.day,
        [
            datetime(2021, 5, 17, 0, 0),
            datetime(2021, 5, 18, 0, 0),
            datetime(2021, 5, 19, 0, 0),
            datetime(2021, 5, 20, 0, 0),
            datetime(2021, 5, 21, 0, 0),
            datetime(2021, 5, 22, 0, 0),
            datetime(2021, 5, 23, 0, 0),
        ],
    ),
    "all_week_start_related_to_may": Example(
        date(2021, 5, 1),
        date(2021, 5, 31),
        Interval.week,
        [
            datetime(2021, 5, 3, 0, 0),
            datetime(2021, 5, 10, 0, 0),
            datetime(2021, 5, 17, 0, 0),
            datetime(2021, 5, 24, 0, 0),
            datetime(2021, 5, 31, 0, 0),
        ],
    ),
    "all_months_for_a_year": Example(
        date(2021, 1, 1),
        date(2021, 12, 31),
        Interval.month,
        [
            datetime(2021, 1, 1, 0, 0),
            datetime(2021, 2, 1, 0, 0),
            datetime(2021, 3, 1, 0, 0),
            datetime(2021, 4, 1, 0, 0),
            datetime(2021, 5, 1, 0, 0),
            datetime(2021, 6, 1, 0, 0),
            datetime(2021, 7, 1, 0, 0),
            datetime(2021, 8, 1, 0, 0),
            datetime(2021, 9, 1, 0, 0),
            datetime(2021, 10, 1, 0, 0),
            datetime(2021, 11, 1, 0, 0),
            datetime(2021, 12, 1, 0, 0),
        ],
    ),
    "tricky_month_start": Example(
        date(2021, 1, 5),
        date(2021, 3, 5),
        Interval.month,
        [datetime(2021, 2, 1, 0, 0), datetime(2021, 3, 1, 0, 0)],
    ),
    "tricky_week_start": Example(
        date(2021, 2, 28),
        date(2021, 3, 1),
        Interval.week,
        [datetime(2021, 3, 1, 0, 0)],
    ),
    "tricky_day": Example(
        date(2021, 2, 28),
        date(2021, 3, 1),
        Interval.day,
        [datetime(2021, 2, 28, 0, 0), datetime(2021, 3, 1, 0, 0)],
    ),
}

if __name__ == "__main__":
    for name, example in EXAMPLES.items():
        try:
            assert calculate_datetimes_between(example.from_date, example.to_date, example.interval) == example.result
            print(f"Case {name} PASSED.")
        except AssertionError:
            print(f"Failed case: {name}")
            print("Expected:")
            pprint(example.result)
            print("Calculated:")
            pprint(calculate_datetimes_between(example.from_date, example.to_date, example.interval))
            print("-" * 80)

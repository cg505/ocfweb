from datetime import date
from datetime import timedelta

from django.shortcuts import render
from ocflib.lab.hours import Day
from ocflib.lab.hours import HOLIDAYS
from ocflib.lab.stats import current_semester_start

from ocfweb.api.hours import display_hours


def get_holidays():
    for start, stop, name, hours in HOLIDAYS:
        # there should be a better way to do this...
        if name in ('Summer Break', 'Winter Break'):
            continue

        day = start
        while start <= day <= stop:
            if date.today() <= day:
                yield (day, name, hours)
            day += timedelta(days=1)


def get_semester():
    """Get the current semester (Fall 2016, Spring 2018, etc.)"""
    start = current_semester_start()
    semester = 'Fall' if start.month > 6 else 'Spring'
    return '{} {}'.format(semester, start.year)


def lab(doc, request):
    return render(
        request,
        'docs/lab.html',
        {
            'title': doc.title,
            'description': (
                'The Open Computing Facility computer lab is a '
                'free and open-source computer lab located on the '
                'UC Berkeley campus, maintained by OCF volunteers.'
            ),
            'hours_this_week': [
                Day.from_date(date.today() + timedelta(days=i))
                for i in range(7)
            ],
            'regular_hours': display_hours(),
            'holidays': list(get_holidays()),
            'semester': get_semester(),
            'SUNDAY': Day.SUNDAY,
            'MONDAY': Day.MONDAY,
            'TUESDAY': Day.TUESDAY,
            'WEDNESDAY': Day.WEDNESDAY,
            'THURSDAY': Day.THURSDAY,
            'FRIDAY': Day.FRIDAY,
            'SATURDAY': Day.SATURDAY,
        },
    )

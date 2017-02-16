#!/usr/bin/python
# -*- coding: utf-8 -*-

# using python 3.5

import calendar
from datetime import datetime

total_lists = 31
list_per_day = 1

weekday_str = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

gaps = []
rev_gaps = [0, 1, 2, 4, 7, 15]

c = calendar.Calendar()
today = datetime.today()
year = today.year
month = today.month
date = today.day
print("year: ", year)
print("month: ", month)
print("date: ", date)

def

def RenderTemplate(planned_days, total_months):
    return None

if __name__ == "__main__":
    planned_days, total_months = GetPlannedDayList(year, month)
    html_output = RenderTemplate(planned_days, total_months)
    with open('cal.html', 'w') as f:
        for line in html_output:
            f.write(line)

    txt_output = GetTemplateRawData(planned_days)
    with open('cal.txt', 'w') as f:
        for line in txt_output:
            f.write(line)

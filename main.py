#!/usr/bin/python
# -*- coding: utf-8 -*-

# using python 3.5

import calendar
from datetime import datetime

cur_list = []
total_lists = []
total_lists_count = 45
list_per_day = 2

for idx in range(1, total_lists_count+1):
    total_lists.append(idx)

for idx in range(1, list_per_day+1):
    cur_list.append(idx)

weekday_str = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

gaps = []
rev_gaps = [0, 1, 3, 7, 15]

c = calendar.Calendar()
today = datetime.today()
year_now = today.year
month_now = today.month
day_now = today.day

def AppendListOfString(src_strings, strings):
    for string in strings:
        src_strings.append(string)
    return src_strings

def GetPlannedDayList(year, month):
    planned_days = []
    total_months = 0

    for month_cnt in range(month, 12):
        total_months += 1
        for date, weekday in c.itermonthdays2(year, month_cnt):
            if date == 0:
                continue
            elif (month == month_now and date < 15):
                continue
            else:
                planned_days.append({'Month': month_cnt, 'Date': date,
                                     'Weekday': weekday, 'Week': weekday_str[weekday], 'New': [], 'Revision': []})

                for list_range in range(0, min(len(planned_days) * list_per_day + 1, total_lists_count), list_per_day):
                    list_numbers = []
                    list_numbers = AppendListOfString(list_numbers, total_lists[list_range:list_range+list_per_day])
                    if list_numbers[-1] == len(planned_days) * list_per_day:
                        planned_days[-1]['New'] = AppendListOfString(planned_days[-1]['New'], list_numbers)
                    if len(planned_days) - list_numbers[-1] / list_per_day in rev_gaps:
                        planned_days[-1]['Revision'] = AppendListOfString(planned_days[-1]['Revision'], list_numbers)

                if len(planned_days[-1]['New']) == 0 and len(planned_days[-1]['Revision']) == 0:
                    return planned_days, total_months


def FormatDateInfo(day, newline='\n'):
    temp_str = '%d-%d-%d-%s:' + newline + '\tNew: ' + len(day['New']) * "%d," + newline + '\tRevision: ' + len(
        day['Revision']) * '%d,' + newline
    pargs = [year_now, day['Month'], day['Date'], day['Week']]
    pargs.extend(day['New'])
    pargs.extend(day['Revision'])
    return temp_str % tuple(pargs)


def GetTemplateRawData(planned_days):
    text_output = []
    for day in planned_days:
        text_output.append(FormatDateInfo(day))
    return text_output


def ClearBlankDatePlaceHolders(line):
    # Clear Blank placeholders
    for i in range(0, 8):
        line = line.replace('{$DAY%d}' % i, '')
    return line


def RenderTemplate(planned_days, total_months):
    base_template = []
    with open('template', 'r') as f:
        for line in f:
            base_template.append(line)

    table_head = base_template[0:3]
    table_end = base_template[-1]
    line_template = base_template[-2]
    new_line = '<br>'

    real_template = []
    current_month = planned_days[0]['Month']

    real_template.extend(table_head)
    real_template[1] = real_template[1].replace("{$YEAR}", str(str(year_now).encode('utf-8')))
    real_template[1] = real_template[1].replace("{$MONTH}", str(current_month))
    real_template.append(line_template)

    for day in planned_days:
        if day['Month'] != current_month:
            real_template[-1] = ClearBlankDatePlaceHolders(real_template[-1])
            current_month = day['Month']
            real_template.append(table_end)
            real_template.append(new_line)
            real_template.extend(table_head)
            real_template[-2] = real_template[-2].replace('{$MONTH}', str(current_month))
            real_template[-2] = real_template[-2].replace('{$YEAR}', str(2017))
            real_template.append(line_template)
        elif day['Weekday'] == 0:
            real_template[-1] = ClearBlankDatePlaceHolders(real_template[-1])
            real_template.append(line_template)
        real_template[-1] = real_template[-1].replace('{$DAY%d}' % (day['Weekday'] + 1), FormatDateInfo(day, '<br>'))
    real_template[-1] = ClearBlankDatePlaceHolders(real_template[-1])
    real_template.append(table_end)

    return real_template


if __name__ == "__main__":
    planned_days, total_months = GetPlannedDayList(year_now, month_now)
    html_output = RenderTemplate(planned_days, total_months)
    with open('cal.html', 'w') as f:
        for line in html_output:
            f.write(line)

    txt_output = GetTemplateRawData(planned_days)
    with open('cal.txt', 'w') as f:
        for line in txt_output:
            f.write(line)

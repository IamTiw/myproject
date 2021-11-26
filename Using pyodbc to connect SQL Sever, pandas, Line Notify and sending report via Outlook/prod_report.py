from prod_setup import *
from datetime import date, timedelta
import pandas as pd

all_data = CsvDatabase.read_csv()
date_target = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')

df = pd.read_csv('Your filename .csv') #<<<<<<<<<<<<<<<<<<<<<<<<< [1/1]
df = df.loc[df.shift_date == date_target]
lines = df.line.unique()

data = [f'\n#Daily Report\nDate: {date_target}']

for line in lines:
    by_shift = df[df.line == line].groupby('shift_name')['good'].sum()
    all_shift = df[df.line == line].groupby('line')['good'].sum()
    shifts = df[df.line == line].shift_name.unique()

    if 'Day' in shifts:
        total_day = by_shift.Day
    else:
        total_day = 0

    if 'Night' in shifts:
        total_night = by_shift.Night
    else:
        total_night = 0

    all_data = [
        f'\n\nLine: {line}'
        f'\nDay: {total_day}'
        f'\nNight: {total_night}'
        f'\nTotal: {all_shift[line]}'
    ]

    data.extend(all_data)

data = ConvertText.convert_list_to_string(data)
Notify.prod_notify(data)
Email.send_email(date_target, data)

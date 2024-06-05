import datetime


def get_current_date() -> str:
    current_date = datetime.date.today()
    current_date = current_date.strftime('%d %B %Y')
    return current_date


def get_current_month():
    current_date = datetime.date.today()
    month = current_date.month
    year = current_date.year
    if month < 10:
        month = '0' + str(month)
    return str(year) + '.' + str(month) + '.' + '01'


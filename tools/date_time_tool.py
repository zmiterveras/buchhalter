import datetime


def get_current_date():
    current_date = datetime.date.today()
    current_date = current_date.strftime('%d %B %Y')
    return current_date

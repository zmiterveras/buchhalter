import datetime
from logging import getLogger

logger = getLogger(__name__)

string_format = '%Y.%m.%d'


def get_current_date(formatting: str = 'default') -> str:
    current_date = datetime.date.today()
    match formatting:
        case 'default':
            current_date = current_date.strftime('%d %B %Y')
        case 'month':
            current_date = current_date.strftime('%b')
        case 'day':
            current_date = current_date.strftime(string_format)
    return current_date


def get_current_month() -> tuple[str, str]:
    current_date = datetime.date.today()
    month = current_date.month
    first_day_current_month = current_date.replace(day=1)
    return first_day_current_month.strftime(string_format), str(month)

def get_start_end_month(next_month_start: str) -> tuple[str, str]:
    date_object = datetime.datetime.strptime(next_month_start, string_format).date()
    last_day = date_object - datetime.timedelta(days=1)
    first_day = last_day.replace(day=1)
    return first_day.strftime(string_format), last_day.strftime(string_format)


def get_last_week(purpose: str ='default') -> str:
    current_date = datetime.date.today()
    last_week = current_date - datetime.timedelta(days=7)
    match purpose:
        case 'default':
            return last_week.strftime(string_format)
        case 'view':
            return last_week.strftime('%d %B %Y')


def get_next_month(month: str) -> str:
    list_month = month.split('.')
    month_start = '.'.join(list_month[:2]) + '.01'
    dt = datetime.date.fromisoformat(month_start.replace('.', '-'))
    dt_next = dt + datetime.timedelta(days=31)
    if dt_next.day != 1:
        dt_next = dt_next.replace(day=1)
    return dt_next.strftime(string_format)

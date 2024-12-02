import datetime
from logging import getLogger


logger = getLogger(__name__)


def get_current_date(formatting: str='default') -> str:
    current_date = datetime.date.today()
    match formatting:
        case 'default':
            current_date = current_date.strftime('%d %B %Y')
        case 'month':
            current_date = current_date.strftime('%b')
        case 'day':
            current_date = current_date.strftime('%Y.%m.%d')
    return current_date


def get_current_month() -> tuple:
    current_date = datetime.date.today()
    month = current_date.month
    year = current_date.year
    if month < 10:
        month = '0' + str(month)
    logger.info('get current date')
    return str(year) + '.' + str(month) + '.' + '01', str(month)


def get_last_week(purpose: str='default') -> str:
    current_date = datetime.date.today()
    last_week = current_date - datetime.timedelta(days=7)
    match purpose:
        case 'default':
            return last_week.strftime('%Y.%m.%d')
        case 'view':
            return last_week.strftime('%d %B %Y')

def get_next_month(month: str) -> str:
    list_month = month.split('.')
    month_start = '.'.join(list_month[:2]) + '.01'
    dt = datetime.date.fromisoformat(month_start.replace('.', '-'))
    dt_next = dt + datetime.timedelta(days=31)
    if dt_next.day != 1:
        dt_next = dt_next.replace(day=1)
    return dt_next.strftime('%Y.%m.%d')







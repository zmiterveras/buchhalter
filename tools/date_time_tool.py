import datetime
from logging import getLogger


logger = getLogger(__name__)


def get_current_date() -> str:
    current_date = datetime.date.today()
    current_date = current_date.strftime('%d %B %Y')
    return current_date


def get_current_month() -> tuple:
    current_date = datetime.date.today()
    month = current_date.month
    year = current_date.year
    if month < 10:
        month = '0' + str(month)
    logger.info('get current date')
    return str(year) + '.' + str(month) + '.' + '01', str(month)


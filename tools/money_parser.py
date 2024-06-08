from logging import getLogger

logger = getLogger(__name__)


def get_view_money(money: int) -> str:
    money_int = str(money // 100)
    money_dec = str(money % 100) if money % 100 > 9 else '0' + str(money % 100)
    logger.info('convert_money')
    return money_int + ',' + money_dec

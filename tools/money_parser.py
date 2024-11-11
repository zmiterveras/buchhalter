from logging import getLogger

logger = getLogger(__name__)


def get_view_money(money: int) -> str:
    sign = None
    if money < 0:
        money = abs(money)
        sign = '-'
    money_int = str(money // 100)
    money_dec = str(money % 100) if money % 100 > 9 else '0' + str(money % 100)
    str_money = money_int + ',' + money_dec if not sign else sign + money_int + ',' + money_dec
    logger.info('convert_money: ' + str_money)
    return str_money

def get_int_dec(money: str) -> (int, int):
    money_list = money.split(',')
    return int(money_list[0]), int(money_list[1])

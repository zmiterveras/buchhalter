from logging import getLogger

logger = getLogger(__name__)


def note_search_parser(search_str: str, field: str = '%(key)s') -> str:
    search_list = search_str.strip().split(' ')
    re_search_str = ''
    search_list_len = len(search_list)
    for num, item in enumerate(search_list):
        ending = '' if search_list_len == 1 or num == search_list_len -1 else ' or '
        if not item.isdigit():
            item_pattern = f'{field} regexp "[{item[0].upper()}{item[0].lower()}]{item[1:]}"{ending}'
        else:
            item_pattern = f'{field} regexp "{item}"{ending}'
        re_search_str += item_pattern
    if search_list_len > 1:
        re_search_str = f'({re_search_str})'
    return f' and {re_search_str}'

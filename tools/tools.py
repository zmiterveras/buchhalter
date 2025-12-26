import re
from logging import getLogger
from menu_languages.menulanguages import MenuLanguages

logger = getLogger(__name__)


def get_category_names(language: str, table: str) -> list:
    match language:
        case 'en':
            return [MenuLanguages.en[name] for name in MenuLanguages.cat_keys_credit] if table == 'expense' \
                else [MenuLanguages.en[name] for name in MenuLanguages.cat_keys_debit]
        case _:
            return [MenuLanguages.ru[name] for name in MenuLanguages.cat_keys_credit] if table == 'expense' \
                else [MenuLanguages.ru[name] for name in MenuLanguages.cat_keys_debit]

def get_explode_list(values: list):
    explode_list = []
    sums = sum(values)
    for i in values:
        if i / sums <= 0.03:
            explode_list.append(0.1)
        else:
            explode_list.append(0.03)
    return explode_list

def regexp_match(pattern: str, input_string: str):
    if input_string is None:
        return False
    return bool(re.search(pattern, input_string))

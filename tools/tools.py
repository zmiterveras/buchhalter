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

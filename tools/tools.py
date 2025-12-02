from logging import getLogger

from menu_languages.menulanguages import MenuLanguages

logger = getLogger(__name__)

def get_category_names(language: str, table: str) -> list:
    match table:
        case 'expense':
            return [MenuLanguages.en[name] for name in MenuLanguages.cat_keys_credit] if language == 'en' \
                else [MenuLanguages.ru[name] for name in MenuLanguages.cat_keys_credit]
        case _:
            return [MenuLanguages.en[name] for name in MenuLanguages.cat_keys_debit] if language == 'en' \
                else [MenuLanguages.ru[name] for name in MenuLanguages.cat_keys_debit]

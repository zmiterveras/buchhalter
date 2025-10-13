from logging import getLogger

logger = getLogger(__name__)


def note_search_parser(search_str: str) -> str:
    search_list = search_str.strip().lower().split(' ')
    query_search_string='LIKE '
    for item in search_list:
        query_search_string += f'%{item}% '
    return query_search_string

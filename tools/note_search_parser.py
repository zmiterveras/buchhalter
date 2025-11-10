from logging import getLogger

logger = getLogger(__name__)


def note_search_parser(search_str: str) -> str:
    # search_list = search_str.strip().lower().split(' ')
    search_list = search_str.strip().split(' ')
    search_string=''
    for item in search_list:
        search_string += f'%{item}%'
    query_search_string = f' LIKE "{search_string}"'
    return query_search_string

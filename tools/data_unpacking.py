from tools.money_parser import get_view_money


def unpacking_expense(expense: list) -> tuple:
    ids = []
    dates = []
    values = []
    categories = []
    for id_note, date, value, category in expense:
        ids.append(id_note)
        dates.append(date)
        values.append(get_view_money(value))
        categories.append(category)
    return ids, dates, values, categories

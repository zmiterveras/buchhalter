from tools.money_parser import get_view_money


def unpacking_expense(expense: list) -> tuple:
    ids = []
    dates = []
    values = []
    categories = []
    notes = []
    for id_note, date, value, category, note in expense:
        ids.append(id_note)
        dates.append(date)
        values.append(get_view_money(value))
        categories.append(category)
        notes.append(note)
    return ids, dates, values, categories, notes

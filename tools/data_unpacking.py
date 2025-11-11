from tools.money_parser import get_view_money


def unpacking(data_list: list) -> tuple:
    ids = []
    dates = []
    values = []
    categories = []
    notes = []
    for id_note, date, value, category, note in data_list:
        ids.append(id_note)
        dates.append(date)
        values.append(get_view_money(value))
        categories.append(category)
        notes.append(note)
    return ids, dates, values, categories, notes

def unpacking_diagram(data_list: list) -> tuple:
    cat_names = []
    values = []
    values_str = []
    for cat_name, value in data_list:
        cat_names.append(cat_name)
        values.append(value)
        values_str.append(get_view_money(value))
    return cat_names, values, values_str


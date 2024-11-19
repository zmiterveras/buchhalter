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

def unpacking_income(income: list) -> tuple:
    ids = []
    salaries = []
    bonuses = []
    gifts = []
    percents = []
    dates = []
    notes = []
    for id_income, salary, bonus, gift, percent, date, note in income:
        ids.append(id_income)
        salaries.append(salary)
        bonuses.append(bonus)
        gifts.append(gift)
        percents.append(percents)
        dates.append(date)
        notes.append(note)
    return ids, salaries, bonuses, gifts, percents, dates, notes

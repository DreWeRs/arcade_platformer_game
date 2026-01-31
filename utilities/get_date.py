from datetime import date


def get_date():
    current_date = date.today()
    return f'{current_date.day}.{current_date.strftime('%m')}.{current_date.year}'

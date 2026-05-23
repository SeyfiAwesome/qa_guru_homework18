from pathlib import Path
from datetime import datetime
import calendar


def get_file_path(file_name: str) -> str:
    return str(
        Path(__file__).parent.joinpath(f'source/{file_name}')
    )


def modify_date_format(year: str, month: str, day: str) -> str:
    if month.isalpha():
        month_number = list(calendar.month_abbr).index(month[:3]) if len(month) == 3 else list(
            calendar.month_name).index(month)
    else:
        month_number = int(month)

    date_object = datetime(int(year), month_number, int(day))
    return date_object.strftime("%d %B,%Y").lstrip('0')
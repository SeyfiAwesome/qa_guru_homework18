from pathlib import Path
from datetime import datetime

def get_file_path(file_name: str) -> str:
    return str(
        Path(__file__).parent.joinpath(f'source/{file_name}')
    )

def modify_date_format(year: str, month: str, day: str) -> str:
    date_object = datetime(int(year), int(month), int(day))
    return date_object.strftime("%d %B,%Y").lstrip('0')

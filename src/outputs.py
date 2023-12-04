import csv
import logging
import datetime as dt

from utils import checking_directory
from prettytable import PrettyTable
from constants import DATETIME_FORMAT, BASE_DIR


def control_output(results, cli_args):
    """Вывод информации."""
    output = cli_args.output
    if output == 'pretty':
        pretty_output(results)
    elif output == 'file':
        file_output(results, cli_args)
    else:
        default_output(results)


def default_output(results):
    """Печатаем список results построчно."""
    for row in results:
        print(*row)


def pretty_output(results):
    """Вывод в табличном представлении."""
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    """Сохранения в фаил [.csv]."""
    results_dir = BASE_DIR / 'results'
    if checking_directory(results_dir):
        parser_mode = cli_args.mode
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f'{parser_mode}_{now_formatted}.csv'
        file_path = results_dir / file_name
        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerows(results)
        logging.info(f'Файл с результатами был сохранён: {file_path}')

from pathlib import Path


MAIN_DOC_URL: str = 'https://docs.python.org/3/'
BASE_DIR: Path = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
PEP_URL = 'https://peps.python.org/'
EXPECTED_STATUS: dict = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}
# Регулярное выражение для функции [latest_versions].
# Выводит версию и статус из строчки.
PATTERN_LATEST_VERSIONS = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
# Регулярное выражение для функции [DOWNLOAD].
# Выводит сылки архивов [zip] или [pdf].
PATTERN_DOWNLOAD = r'.+pdf-a4\.zip$'
PARSER_PARAMETER = 'lxml'

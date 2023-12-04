import re
import logging
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from constants import (
    BASE_DIR,
    MAIN_DOC_URL,
    PEP_URL,
    EXPECTED_STATUS,
    PATTERN_LATEST_VERSIONS,
    PARSER_PARAMETER,
    PATTERN_DOWNLOAD,
)
from outputs import control_output
from configs import configure_argument_parser, configure_logging
from utils import get_response, find_tag, checking_directory
from exceptions import ParserFindTagException
from enums import table_headers as th


def get_array_data(session, url, throw_exception=True):
    """Собираю данные страници."""
    response = session.get(url)
    response.encoding = 'utf-8'
    response = get_response(session, url)
    if response is None:
        if throw_exception:
            raise ParserFindTagException(
                f'Не смог получить данных со страници [{url}].'
            )
        else:
            return False
    return BeautifulSoup(response.text, features=PARSER_PARAMETER)


def whats_new(session) -> list:
    """Собирать о нововведениях в Python."""
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_array_data(session, whats_new_url)
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )
    results = th.headers.whats_new.value
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        soup = get_array_data(session, version_link, throw_exception=False)
        if not soup:
            continue
        h1 = find_tag(soup, 'h1')
        dl = soup.find('dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text.encode('utf-8')))
    return results


def latest_versions(session) -> list:
    """Извлекаем изстраницы номер версии и статус Python."""
    soup = get_array_data(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, 'div', attrs={'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    ul = ul_tags[0]
    if 'All versions' not in ul.text:
        raise ParserFindTagException('Ничего не нашлось url:[-].')
    a_tags = ul.find_all('a')
    results = th.headers.latest_versions.value
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(PATTERN_LATEST_VERSIONS, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))
    return results


def download(session) -> None:
    """Скачать свежию документацию по Python."""
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = get_array_data(session, downloads_url)
    main_tag = find_tag(soup, 'div', attrs={'role': 'main'})
    table_tag = find_tag(main_tag, 'table', attrs={'class': 'docutils'})
    pdf_a4_tag = table_tag.find('a', {'href': re.compile(PATTERN_DOWNLOAD)})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    if checking_directory(downloads_dir):
        archive_path = downloads_dir / filename
        response = session.get(archive_url)
        with open(archive_path, 'wb') as file:
            file.write(response.content)
        logging.info(f'Архив был загружен и сохранён: {archive_path}')


def parse_status_type_from_page(url=None) -> dict:
    """Парсим статус и тайп со страницы PEP."""
    type_status = {}
    session = requests_cache.CachedSession()
    response = session.get(PEP_URL + url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, features=PARSER_PARAMETER)
    teg_dl = soup.find('dl')
    teg_dt = teg_dl.find_all('dt')
    teg_dd = teg_dl.find_all('dd')
    for i in range(len(teg_dt)):
        if teg_dt[i].text in ['Status:', 'Type:']:
            type_status[teg_dt[i].text[:-1]] = teg_dd[i].text
    if type_status is not None:
        return type_status['Status']


def conclusion_list(number_statuses) -> list:
    """Подготовка для вывод списка PEP."""
    sum = 0
    results = th.headers.conclusion_list.value
    number_statuses = sorted(number_statuses.items())
    for k, v in number_statuses:
        sum += v
        if k == '':
            results.append(("''", v))
        else:
            results.append((k, v))
    results.append(('Total:', sum))
    return results


def list_inconsistencies(incorrect_statuses):
    """Показать список не соотвтствующих статусов PEP."""
    logging.info('Несовпадающие статусы:')
    for incorrect_status in incorrect_statuses:
        logging.info((PEP_URL + incorrect_status['url']))
        logging.info(('Статус в карточке:', incorrect_status['status']))
        logging.info(
            ('Ожидаемые статусы:',
             f"['{incorrect_status['ls']}', '{incorrect_status['ps']}']")
        )


def collecting_list(teg_tbody):
    """распределяет полученуе даные PEP."""
    number_statuses = {}
    incorrect_status = []
    for x in tqdm(teg_tbody):
        teg_tr = x.find_all('tr')
        for v in teg_tr:
            teg_abbr = v.find('abbr')
            if teg_abbr is not None:
                status_general = teg_abbr['title'].split()
            else:
                status_general = ['', '']
            a_href = v.find('a')
            if a_href is not None:
                status = parse_status_type_from_page(a_href['href'])
                if status_general[-1] != status:
                    incorrect_status.append({
                        'url': a_href['href'],
                        'status': status,
                        'ls': status_general[0][:-1],
                        'ps': status_general[-1]}
                    )
                status_general = status_general[-1]
                for k, v in EXPECTED_STATUS.items():
                    if status_general in v:
                        if k in number_statuses:
                            number_statuses[k] += 1
                        else:
                            number_statuses[k] = 1
    return number_statuses, incorrect_status


def pep(session) -> list:
    """спарсить и подсчитать количество каждого статуса PEP."""
    soup = get_array_data(session, PEP_URL)
    teg_tbody = soup.find_all('tbody')
    number_statuses, incorrect_status = collecting_list(teg_tbody)
    if len(incorrect_status) > 0:
        list_inconsistencies(incorrect_status)
    return conclusion_list(number_statuses)


MODE_TO_FUNCTION: dict = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()

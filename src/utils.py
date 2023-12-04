import os
import logging
from requests import RequestException
from exceptions import ParserFindTagException, ErrorCreatingDirectoryException


def get_response(session, url):
    """Перехват ошибки RequestException."""
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    """Перехват ошибки поиска тегов."""
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def checking_directory(dir):
    """Проверка каталога."""
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except OSError:
            text_error = f'Не получилось создать каталог: {dir}'
            raise ErrorCreatingDirectoryException(text_error)

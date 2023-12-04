class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class ErrorCreatingDirectoryException(Exception):
    """Вызывается, когда неполучается создать директорию."""
    pass

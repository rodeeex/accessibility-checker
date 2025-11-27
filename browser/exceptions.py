class PageFetchTimeout(Exception):
    """
    Возникает, когда превышен интервал ожидания при загрузке страницы
    """
    def __init__(self, url: str, timeout: int):
        super().__init__(f"Превышен таймаут {timeout} мс при загрузке страницы: {url}")
        self.url = url
        self.timeout = timeout


class PageFetchError(Exception):
    """
    Общее исключение при ошибке загрузки страницы
    """
    def __init__(self, url: str, original_exception: Exception):
        super().__init__(f"Ошибка при загрузке страницы {url}: {original_exception}")
        self.url = url
        self.original_exception = original_exception
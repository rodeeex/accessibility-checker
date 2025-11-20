import os
import shutil
from datetime import datetime
from typing import Optional
from .report import make_report


def save_report_to_file(issues, url: str, report_type: str,
                       output_path: Optional[str] = None,
                       filename: Optional[str] = None) -> str:
    """
    Генерирует и сохраняет отчет в файл

    :param issues: Список найденных нарушений
    :param url: URL проверенной страницы
    :param report_type: Тип отчета ('json', 'html', 'pdf')
    :param output_path: Путь для сохранения (по умолчанию текущая директория)
    :param filename: Имя файла (автогенерируется если не указано)
    :return: Полный путь к сохраненному файлу
    """
    if report_type not in ['json', 'html', 'pdf']:
        raise ValueError("Сохранение поддерживается только для форматов: json, html, pdf")

    # Определяем путь для сохранения
    if output_path is None:
        output_path = os.getcwd()

    # Создаем директорию если её нет
    os.makedirs(output_path, exist_ok=True)

    # Генерируем имя файла если не указано
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = _extract_domain(url)
        filename = f"accessibility_report_{domain}_{timestamp}.{report_type}"

    # Полный путь к файлу
    full_path = os.path.join(output_path, filename)

    # Генерируем отчет и сохраняем
    if report_type == 'pdf':
        # PDF генератор уже создает файл, просто перемещаем его
        temp_pdf_path = make_report(issues, url, 'pdf')
        shutil.move(temp_pdf_path, full_path)
    else:
        # Для JSON и HTML генерируем контент и записываем в файл
        report_content = make_report(issues, url, report_type)

        encoding = 'utf-8'
        with open(full_path, 'w', encoding=encoding) as f:
            f.write(report_content)

    return full_path


def save_multiple_reports(issues, url: str, report_types: list,
                         output_path: Optional[str] = None,
                         filename_prefix: Optional[str] = None) -> dict:
    """
    Сохраняет отчеты в нескольких форматах одновременно

    :param issues: Список найденных нарушений
    :param url: URL проверенной страницы
    :param report_types: Список типов отчетов для генерации
    :param output_path: Путь для сохранения
    :param filename_prefix: Префикс для имен файлов
    :return: Словарь с путями к созданным файлам {тип: путь}
    """
    if output_path is None:
        output_path = os.getcwd()

    # Создаем директорию если её нет
    os.makedirs(output_path, exist_ok=True)

    # Генерируем префикс если не указан
    if filename_prefix is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = _extract_domain(url)
        filename_prefix = f"accessibility_report_{domain}_{timestamp}"

    saved_files = {}

    for report_type in report_types:
        if report_type not in ['json', 'html', 'pdf', 'console']:
            continue

        try:
            if report_type == 'console':
                # Сохраняем консольный отчет как текстовый файл
                filename = f"{filename_prefix}.txt"
                full_path = os.path.join(output_path, filename)

                report_content = make_report(issues, url, 'console')
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(report_content)

                saved_files[report_type] = full_path
            else:
                # Используем основную функцию сохранения
                filename = f"{filename_prefix}.{report_type}"
                full_path = save_report_to_file(issues, url, report_type,
                                              output_path, filename)
                saved_files[report_type] = full_path

        except Exception as e:
            print(f"Ошибка при сохранении {report_type} отчета: {e}")

    return saved_files


def create_report_archive(issues, url: str, output_path: Optional[str] = None,
                         archive_name: Optional[str] = None) -> str:
    """
    Создает архив со всеми типами отчетов

    :param issues: Список найденных нарушений
    :param url: URL проверенной страницы
    :param output_path: Путь для сохранения архива
    :param archive_name: Имя архива
    :return: Путь к созданному архиву
    """
    import zipfile
    import tempfile

    if output_path is None:
        output_path = os.getcwd()

    if archive_name is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = _extract_domain(url)
        archive_name = f"accessibility_reports_{domain}_{timestamp}.zip"

    # Создаем временную директорию для отчетов
    with tempfile.TemporaryDirectory() as temp_dir:
        # Генерируем все типы отчетов
        report_files = save_multiple_reports(
            issues, url,
            ['json', 'html', 'pdf', 'console'],
            temp_dir
        )

        # Создаем архив
        archive_path = os.path.join(output_path, archive_name)
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for report_type, file_path in report_files.items():
                # Добавляем файл в архив с оригинальным именем
                arcname = os.path.basename(file_path)
                zipf.write(file_path, arcname)

        return archive_path


def _extract_domain(url: str) -> str:
    """Извлекает доменное имя из URL для использования в имени файла"""
    from urllib.parse import urlparse

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        # Убираем www. и заменяем точки на подчеркивания
        domain = domain.replace('www.', '').replace('.', '_')
        # Ограничиваем длину и убираем недопустимые символы
        domain = ''.join(c for c in domain if c.isalnum() or c == '_')[:20]
        return domain if domain else 'website'
    except:
        return 'website'


def get_reports_directory() -> str:
    """Возвращает стандартную директорию для сохранения отчетов"""
    reports_dir = os.path.join(os.getcwd(), 'accessibility_reports')
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir

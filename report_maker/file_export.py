import os
from pathlib import Path
from urllib.parse import urlparse
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
    :param report_type: Тип отчета ('json', 'html')
    :param output_path: Путь для сохранения (по умолчанию текущая директория)
    :param filename: Имя файла (автогенерируется если не указано)
    :return: Полный путь к сохраненному файлу
    """
    if report_type not in ['json', 'html']:
        raise ValueError("Сохранение поддерживается только для форматов: json, html")

    if output_path is None:
        output_path = get_reports_directory()
    else:
        output_path = str(output_path)

    os.makedirs(output_path, exist_ok=True)

    if filename:
        filename = Path(filename).name
        full_path = os.path.join(output_path, filename)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = _extract_domain(url)
        ext = report_type
        filename = f"accessibility_report_{domain}_{timestamp}.{ext}"
        full_path = os.path.join(output_path, filename)

    report_content = make_report(issues, url, report_type)

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    return full_path


def _extract_domain(url: str) -> str:
    """Извлекает доменное имя из URL для использования в имени файла"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        domain = domain.replace('www.', '').replace('.', '_')
        domain = ''.join(c for c in domain if c.isalnum() or c == '_')[:20]
        return domain if domain else 'website'
    except:
        return 'website'


def get_reports_directory() -> str:
    """Возвращает стандартную директорию для сохранения отчетов"""
    reports_dir = os.path.join(os.getcwd(), 'accessibility_reports')
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir

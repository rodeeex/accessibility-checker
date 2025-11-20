import os
from jinja2 import Environment, FileSystemLoader, select_autoescape


def generate_html_report(report_data: dict) -> str:
    """
    Генерирует HTML отчет

    :param report_data: Данные для отчета
    :return: HTML строка с отчетом
    """
    # Получаем путь к шаблону
    template_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(template_dir, "report_template.html")

    # Настраиваем Jinja2 окружение
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )

    # Загружаем шаблон
    template = env.get_template("report_template.html")

    # Подготавливаем данные для шаблона
    template_data = _prepare_template_data(report_data)

    # Рендерим шаблон
    return template.render(**template_data)


def _prepare_template_data(report_data: dict) -> dict:
    """Подготавливает данные для шаблона"""
    # Получаем сводку по уровням
    level_summary = _get_level_summary(report_data["issues"])

    return {
        'url': report_data['url'],
        'timestamp': _format_timestamp(report_data['timestamp']),
        'total_issues': report_data['total_issues'],
        'level_a_count': level_summary.get('A', 0),
        'level_aa_count': level_summary.get('AA', 0),
        'level_aaa_count': level_summary.get('AAA', 0),
        'issues': report_data['issues']
    }


def _get_level_summary(grouped_issues: list) -> dict:
    """Создает сводку по уровням критичности"""
    summary = {"A": 0, "AA": 0, "AAA": 0}
    for group in grouped_issues:
        level = group["level"]
        if level in summary:
            summary[level] += group["count"]
    return summary


def _format_timestamp(timestamp: str) -> str:
    """Форматирует временную метку для красивого отображения"""
    from datetime import datetime
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%d.%m.%Y %H:%M:%S")
    except:
        return timestamp

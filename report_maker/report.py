from typing import List
from datetime import datetime
from rules.base import Issue


def make_report(issues: List[Issue], url: str, report_type: str = 'console') -> str:
    """
    Генерирует отчет о проблемах доступности в зависимости от типа

    :param issues: Список найденных нарушений
    :param url: URL проверенной страницы
    :param report_type: Тип отчета ('console', 'json', 'html', 'pdf')
    :return: Сгенерированный отчет в виде строки (для pdf - путь к файлу)
    """
    # Группируем и сортируем проблемы
    grouped_issues = _group_and_sort_issues(issues)
    
    # Подготавливаем базовые данные для отчета
    report_data = {
        'url': url,
        'timestamp': datetime.now().isoformat(),
        'total_issues': len(issues),
        'issues': grouped_issues
    }
    
    # Вызов по типу отчета
    if report_type == 'console':
        from .console import generate_console_report
        return generate_console_report(report_data)
    elif report_type == 'json':
        from .json import generate_json_report
        return generate_json_report(report_data)
    elif report_type == 'html':
        from .html import generate_html_report
        return generate_html_report(report_data)
    elif report_type == 'pdf':
        from .pdf import generate_pdf_report
        return generate_pdf_report(report_data)
    else:
        raise ValueError(f"Неподдерживаемый тип отчета: {report_type}")


def _group_and_sort_issues(issues: List[Issue]) -> List:
    """
    Группирует и сортирует нарушения по критичности и типу

    :param issues: Список нарушений
    :return: Отсортированный и сгруппированный список нарушений
    """
    # Определяем приоритет уровней критичности
    level_priority = {'AAA': 3, 'AA': 2, 'A': 1}
    
    # Сортируем по уровню критичности (сначала самые критичные)
    sorted_issues = sorted(issues, key=lambda x: level_priority.get(x.level, 0), reverse=True)
    
    # Группируем по названию правила и критерию
    groups = {}
    for issue in sorted_issues:
        key = (issue.name, issue.criterion, issue.level)
        if key not in groups:
            groups[key] = {
                'name': issue.name,
                'criterion': issue.criterion,
                'level': issue.level,
                'count': 0,
                'issues': []
            }
        groups[key]['count'] += 1
        groups[key]['issues'].append({
            'element': issue.element,
            'line': issue.line,
            'message': issue.message,
            'recommendation': issue.recommendation
        })
    
    # Преобразуем в список и сортируем группы по критичности
    grouped_list = list(groups.values())
    grouped_list.sort(key=lambda x: level_priority.get(x['level'], 0), reverse=True)
    
    return grouped_list

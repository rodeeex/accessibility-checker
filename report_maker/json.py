import json


def generate_json_report(report_data: dict) -> str:
    """
    Генерирует JSON отчет

    :param report_data: Данные для отчета
    :return: JSON строка с отчетом
    """
    # Создаем структуру JSON отчета
    json_report = {
        "report_info": {
            "url": report_data["url"],
            "timestamp": report_data["timestamp"],
            "total_issues": report_data["total_issues"]
        },
        "summary": {
            "by_level": _get_issues_summary_by_level(report_data["issues"]),
            "by_criterion": _get_issues_summary_by_criterion(report_data["issues"])
        },
        "issues": report_data["issues"]
    }
    
    return json.dumps(json_report, ensure_ascii=False, indent=2)


def _get_issues_summary_by_level(grouped_issues: list) -> dict:
    """Создает сводку по уровням критичности"""
    summary = {"A": 0, "AA": 0, "AAA": 0}
    for group in grouped_issues:
        level = group["level"]
        if level in summary:
            summary[level] += group["count"]
    return summary


def _get_issues_summary_by_criterion(grouped_issues: list) -> dict:
    """Создает сводку по критериям WCAG"""
    summary = {}
    for group in grouped_issues:
        criterion = group["criterion"]
        if criterion not in summary:
            summary[criterion] = 0
        summary[criterion] += group["count"]
    return summary

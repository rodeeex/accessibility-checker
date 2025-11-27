from colorama import Fore, Style, init

init(autoreset=True)


def generate_console_report(report_data: dict) -> str:
    """
    Генерирует консольный отчет

    :param report_data: Данные для отчета
    :return: Отформатированный текстовый отчет
    """
    lines = []

    lines.append("=" * 80)
    lines.append(f"{Fore.CYAN}{Style.BRIGHT}ОТЧЕТ О ПРОВЕРКЕ ДОСТУПНОСТИ")
    lines.append("=" * 80)

    lines.append(f"URL: {Fore.BLUE}{report_data['url']}")
    lines.append(f"Время проверки: {report_data['timestamp']}")
    lines.append(f"Общее количество проблем: {Fore.RED}{report_data['total_issues']}")
    lines.append("")

    summary = _get_level_summary(report_data["issues"])
    lines.append(f"{Fore.YELLOW}{Style.BRIGHT}СВОДКА ПО УРОВНЯМ:")
    lines.append("-" * 30)
    for level, count in summary.items():
        color = _get_level_color(level)
        lines.append(f"Уровень {color}{level}: {count} проблем(а)")
    lines.append("")

    if report_data["issues"]:
        lines.append(f"{Fore.YELLOW}{Style.BRIGHT}ДЕТАЛИ ПРОБЛЕМ:")
        lines.append("-" * 40)

        for i, group in enumerate(report_data["issues"], 1):
            level_color = _get_level_color(group["level"])

            lines.append(f"\n{i}. {Fore.WHITE}{Style.BRIGHT}{group['name']}")
            lines.append(f"   Критерий WCAG: {Fore.CYAN}{group['criterion']}")
            lines.append(f"   Уровень: {level_color}{group['level']}")
            lines.append(f"   Количество: {Fore.RED}{group['count']}")

            for j, issue in enumerate(group["issues"][:3], 1):
                lines.append(f"   {j}) Элемент: {Fore.MAGENTA}{issue['element']}")
                lines.append(f"      Строка: {issue['line']}")
                lines.append(f"      Описание: {issue['message']}")
                lines.append(f"      Рекомендация: {Fore.GREEN}{issue['recommendation']}")

            if len(group["issues"]) > 3:
                lines.append(f"   ... и еще {len(group['issues']) - 3} проблем(а)")
    else:
        lines.append(f"{Fore.GREEN}{Style.BRIGHT}Проблемы доступности не найдены!")

    lines.append("\n" + "=" * 80)

    return "\n".join(lines)


def _get_level_summary(grouped_issues: list) -> dict:
    """Создает сводку по уровням критичности"""
    summary = {"A": 0, "AA": 0, "AAA": 0}
    for group in grouped_issues:
        level = group["level"]
        if level in summary:
            summary[level] += group["count"]
    return summary


def _get_level_color(level: str) -> str:
    """Возвращает цвет для уровня критичности"""
    colors = {
        "A": Fore.YELLOW,
        "AA": Fore.RED,
        "AAA": Fore.MAGENTA
    }
    return colors.get(level, Fore.WHITE)

from typing import List
from .base import WCAGRule, Issue


class KeyboardFocusOrderRule(WCAGRule):
    name = "Focus Order"
    criterion = "2.4.3"
    level = "A"

    def check(self, html: str) -> List[Issue]:
        """
        Проверяет, что порядок фокуса логичен
        """
        issues = []
        soup = self._parse(html)

        for element in soup.select('[tabindex]'):
            try:
                tabindex_value = int(element.get('tabindex'))
                if tabindex_value > 0:
                    issues.append(self._issue(
                        element,
                        f'Элемент имеет положительный tabindex={tabindex_value}',
                        'Использование tabindex > 0 может нарушить логический порядок фокуса. Оставьте tabindex="0" или удалите атрибут',
                        html
                    ))
            except (ValueError, TypeError):
                issues.append(self._issue(
                    element,
                    'Некорректное значение tabindex',
                    'Используйте числовое значение tabindex',
                    html
                ))

        return issues
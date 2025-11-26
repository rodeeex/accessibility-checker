from typing import List
from .base import WCAGRule, Issue

class KeyboardFocusOrderRule(WCAGRule):
    name: str = "Keyboard Focus Order"
    criterion: str = "2.1.2"
    level: str = "A"

    def check(self, html: str) -> List[Issue]:
        """
        Проверяет, что фокус клавиатуры перемещается по странице в логическом порядке.
        """
        issues: List[Issue] = []
        soup = self._parse(html)

        interactive_elements = soup.select('[tabindex]')
        for element in interactive_elements:
            tabindex = element.get('tabindex')
            if tabindex is not None:
                try:
                    tabindex_value = int(tabindex)
                    if tabindex_value < 0:
                        issues.append(self._issue(
                            element,
                            "Элемент имеет отрицательный tabindex",
                            "Установите tabindex >= 0 для обеспечения правильной последовательности навигации",
                            html
                        ))
                except ValueError:
                    issues.append(self._issue(
                        element,
                        "Некорректное значение tabindex",
                        "Используйте числовое значение tabindex",
                        html
                    ))

        return issues

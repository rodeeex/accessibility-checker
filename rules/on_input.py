from typing import List
from .base import WCAGRule, Issue

class OnInputRule(WCAGRule):
    name: str = "On Input"
    criterion: str = "3.2.2"
    level: str = "A"

    def check(self, html: str) -> List[Issue]:
        """
        Проверяет HTML на неожиданные изменения при вводе данных в элементы управления.
        """
        issues: List[Issue] = []
        soup = self._parse(html)

        for element in soup.find_all(['input', 'select', 'textarea']):
            if element.has_attr('onchange'):
                issues.append(self._issue(
                    element,
                    "Изменение значения без подтверждения или уведомления",
                    "Обеспечьте подтверждение изменений или уведомление пользователя при изменении значений",
                    html
                ))

        return issues

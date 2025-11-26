from typing import List
from .base import WCAGRule, Issue


class FocusVisibleRule(WCAGRule):
    name = "Focus Visible"
    criterion = "2.4.7"
    level = "AA"

    def check(self, html: str) -> List[Issue]:
        """
        Проверяет отключение видимого фокуса
        """
        issues = []
        soup = self._parse(html)

        for elem in soup.find_all(style=True):
            style = elem['style'].replace(" ", "").lower()

            if "outline:none" in style or "outline:0" in style:
                issues.append(self._issue(
                    elem,
                    "Элемент отключает видимый фокус (outline:none)",
                    "Не скрывайте outline без предоставления альтернативного видимого фокуса",
                    html
                ))

        return issues
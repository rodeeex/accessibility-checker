from .base import WCAGRule, Issue
from typing import List


class ResizeTextRule(WCAGRule):
    name = "Resize Text"
    criterion = "1.4.4"
    level = "AA"

    def check(self, html: str) -> List[Issue]:
        """
        Проверяет наличие фиксированного размера шрифта,
        который мешает корректному масштабированию.
        """
        issues = []
        soup = self._parse(html)

        for elem in soup.find_all(style=True):
            style = elem["style"].lower()

            if "font-size" in style and "px" in style:
                issues.append(self._issue(
                    elem,
                    "Использован фиксированный размер шрифта (px)",
                    "Используйте относительные единицы (em, rem, %) для масштабируемости текста",
                    html
                ))

        return issues

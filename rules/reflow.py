from typing import List
from .base import WCAGRule, Issue


class ReflowRule(WCAGRule):
    name = "Reflow"
    criterion = "1.4.10"
    level = "AA"

    def check(self, html: str) -> List[Issue]:
        """
        Проверить наличие фиксированных ширин, которые могут вызвать горизонтальный скролл
        при сжатии экрана (inline-стили в px)
        """
        import re
        issues = []
        soup = self._parse(html)

        for elem in soup.find_all():
            style = elem.get("style", "")
            m = re.search(r"width:\s*(\d+)px", style)
            if m:
                w = int(m.group(1))
                if w > 320:
                    issues.append(self._issue(
                        elem,
                        f"Элемент имеет фиксированную ширину {w}px, что нарушает reflow",
                        "Используйте относительные единицы (%, vw) вместо фиксированных",
                        html
                    ))

        return issues
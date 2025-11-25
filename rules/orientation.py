from typing import List
from .base import WCAGRule, Issue


class OrientationRule(WCAGRule):
    name = "Orientation"
    criterion = "1.3.4"
    level = "AA"

    def check(self, html: str) -> List[Issue]:
        """
        Проверить отсутствие ограничения ориентации экрана
        """
        issues = []
        soup = self._parse(html)

        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if viewport and viewport.get('content'):
            content = viewport['content'].lower()
            if 'width' in content and 'height' not in content and 'orientation' not in content:
                if 'device-width' not in content:
                    issues.append(self._issue(
                        viewport,
                        'Meta viewport может ограничивать ориентацию экрана',
                        'Убедитесь, что контент доступен как в портретной, так и в ландшафтной ориентации. Используйте content="width=device-width, initial-scale=1" без жёстких значений',
                        html
                    ))
        return issues
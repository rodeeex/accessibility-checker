from typing import List
from .base import WCAGRule, Issue


class ButtonAccessibilityRule(WCAGRule):
    name = "Name, Role, Value"
    criterion = "4.1.2"
    level = "AA"

    def check(self, html: str) -> List[Issue]:
        """
        Проверить доступность кнопок
        """
        issues = []
        soup = self._parse(html)

        for button in soup.find_all('button'):
            button_text = button.get_text(strip=True)
            aria_label = button.get('aria-label', '').strip()
            title = button.get('title', '').strip()

            if not button_text and not aria_label and not title:
                img = button.find('img')
                if img and img.has_attr('alt') and img['alt'].strip():
                    continue

                if button.has_attr('aria-labelledby'):
                    continue

                issues.append(self._issue(
                    button,
                    'Кнопка не имеет доступного имени',
                    'Добавьте текст внутри кнопки, атрибута aria-label или alt (к изображению)',
                    html
                ))

        for elem in soup.find_all(attrs={'role': 'button'}):
            if elem.name == 'button':
                continue

            elem_text = elem.get_text(strip=True)
            aria_label = elem.get('aria-label', '').strip()

            if not elem_text and not aria_label:
                issues.append(self._issue(
                    elem,
                    f'Элемент <{elem.name}> с role="button" не имеет доступного имени',
                    'Добавьте текст или aria-label для описания действия',
                    html
                ))

        return issues

from typing import List
from .base import WCAGRule, Issue


class LinkAccessibilityRule(WCAGRule):
    name = "Link Purpose (In Context)"
    criterion = "2.4.4"
    level = "A"

    def check(self, html: str) -> List[Issue]:
        """
        Проверить доступность ссылок (исключая якорные цели)
        """
        issues = []
        soup = self._parse(html)

        for link in soup.find_all('a'):
            href = link.get('href', '').strip()

            if not href or href == '#':
                if link.has_attr('name') or link.has_attr('id'):
                    continue

            if not link.has_attr('href'):
                issues.append(self._issue(
                    link,
                    'Ссылка не имеет атрибута href',
                    'Добавьте атрибут href или используйте <button> вместо <a>',
                    html
                ))
                continue

            link_text = link.get_text(strip=True)
            aria_label = link.get('aria-label', '').strip()
            title = link.get('title', '').strip()

            if not link_text and not aria_label and not title:
                img = link.find('img')
                if img and img.get('alt', '').strip():
                    continue

                issues.append(self._issue(
                    link,
                    'Ссылка не содержит текста или альтернативного описания',
                    'Добавьте текст, aria-label или alt к изображению внутри ссылки',
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
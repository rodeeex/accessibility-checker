from typing import List
from .base import WCAGRule, Issue


class ImageAltTextRule(WCAGRule):
    name = "Image Alt Text"
    criterion = "1.1.1"
    level = "A"

    def check(self, html: str) -> List[Issue]:
        """
        Проверить наличие атрибута alt у всех изображений
        """
        issues = []
        soup = self._parse(html)

        for img in soup.find_all('img'):
            if not img.has_attr('alt'):
                issues.append(self._issue(
                    img,
                    "Изображение не имеет атрибута alt",
                    "Добавьте атрибут alt с описательным текстом или пустой alt=\"\" для декоративных изображений",
                    html
                ))
            elif img.get('alt', '').lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.bmp')):
                issues.append(self._issue(
                    img,
                    f"Атрибут alt содержит имя файла: '{img.get('alt')}'",
                    "Замените имя файла на осмысленное описание содержимого изображения",
                    html
                ))

        return issues
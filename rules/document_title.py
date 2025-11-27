from typing import List
from .base import WCAGRule, Issue


class DocumentTitleRule(WCAGRule):
    name = "Page Titled"
    criterion = "2.4.2"
    level = "A"

    def check(self, html: str) -> List[Issue]:
        """
        Проверить наличие и содержимое тега <title>
        """
        issues = []
        soup = self._parse(html)
        title_tag = soup.find('title')

        if not title_tag:
            issues.append(Issue(
                name=self.name,
                criterion=self.criterion,
                level=self.level,
                element='title',
                line=0,
                message='Отсутствует тег <title> в документе',
                recommendation='Добавьте тег <title> в секцию <head> с описательным заголовком страницы'
            ))
        else:
            title_text = title_tag.get_text(strip=True)

            if not title_text:
                issues.append(self._issue(
                    title_tag,
                    'Тег <title> пустой',
                    'Добавьте осмысленный заголовок, описывающий содержимое страницы',
                    html
                ))

        return issues
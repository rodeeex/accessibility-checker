from typing import List
from .base import WCAGRule, Issue


class HtmlLangRule(WCAGRule):
    name = "Language of Page"
    criterion = "3.1.1"
    level = "A"

    def check(self, html: str) -> List[Issue]:
        """
        Проверить наличие атрибута lang у тега <html>
        """
        issues = []
        soup = self._parse(html)
        html_tag = soup.find('html')

        if not html_tag:
            issues.append(Issue(
                name=self.name,
                criterion=self.criterion,
                level=self.level,
                element='html',
                line=1,
                message='Отсутствует тег <html>',
                recommendation='Убедитесь, что страница имеет правильную HTML-структуру с тегом <html>'
            ))
        elif not html_tag.has_attr('lang'):
            issues.append(self._issue(
                html_tag,
                "Тег <html> не имеет атрибута lang",
                'Добавьте атрибут lang с кодом языка (к примеру, lang="ru" или lang="en")',
                html
            ))
        elif not html_tag.get('lang', '').strip():
            issues.append(self._issue(
                html_tag,
                "Атрибут lang тега <html> пустой",
                'Укажите правильный код языка в атрибуте lang',
                html
            ))

        return issues
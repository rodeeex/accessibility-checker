from typing import List
from .base import WCAGRule, Issue


class HeadingsHierarchyRule(WCAGRule):
    name = "Info and Relationships"
    criterion = "1.3.1"
    level = "A"

    def check(self, html: str) -> List[Issue]:
        """
        Проверить правильность иерархии заголовков (h1-h6)
        """
        issues = []
        soup = self._parse(html)
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        if not headings:
            return issues

        h1_count = len([h for h in headings if h.name == 'h1'])
        if h1_count == 0:
            issues.append(Issue(
                name=self.name,
                criterion=self.criterion,
                level=self.level,
                element='h1',
                line=0,
                message='На странице отсутствует заголовок h1',
                recommendation='Добавьте единственный заголовок h1 с основной темой страницы'
            ))
        elif h1_count > 1:
            for h1 in soup.find_all('h1')[1:]:
                issues.append(self._issue(
                    h1,
                    f'На странице несколько заголовков h1 (найдено {h1_count})',
                    'Используйте только один h1-элемент на странице для основного заголовка',
                    html
                ))

        prev_level = 0
        for heading in headings:
            current_level = int(heading.name[1])

            if prev_level > 0 and current_level > prev_level + 1:
                issues.append(self._issue(
                    heading,
                    f'Пропущен уровень заголовка: после h{prev_level} идёт h{current_level}',
                    f'Следует использовать h{prev_level + 1} вместо h{current_level} для правильной иерархии',
                    html
                ))

            prev_level = current_level

        for heading in headings:
            if not heading.get_text(strip=True):
                issues.append(self._issue(
                    heading,
                    f'Заголовок <{heading.name}> пустой',
                    'Добавьте осмысленный текст в заголовок',
                    html
                ))

        return issues

from typing import List
from .base import WCAGRule, Issue


class MultipleWaysRule(WCAGRule):
    name = "Multiple Ways"
    criterion = "2.4.5"
    level = "AA"

    def check(self, html: str) -> List[Issue]:
        """
        Проверить наличие поисковой формы на странице
        """
        issues = []
        soup = self._parse(html)

        search_role = soup.find(attrs={'role': 'search'})
        search_input = soup.find('input', attrs={'type': 'search'})

        search_form = soup.find('form', attrs={
            'class': lambda c: c and 'search' in str(c).lower(),
        }) or soup.find('form', attrs={
            'id': lambda i: i and 'search' in str(i).lower(),
        })

        if not search_role and not search_input and not search_form:
            issues.append(Issue(
                name=self.name,
                criterion=self.criterion,
                level=self.level,
                element='search',
                line=0,
                message='На странице отсутствует функция поиска',
                recommendation='Добавьте поисковую форму с role="search" или input type="search"'
            ))

        return issues

from typing import List
from .base import WCAGRule, Issue


class MultipleWaysRule(WCAGRule):
    name = "Multiple Ways"
    criterion = "2.4.5"
    level = "AA"

    def check(self, html: str) -> List[Issue]:
        """
        Проверить наличие нескольких способов навигации (поиск, навигация, карта сайта)
        """
        issues = []
        soup = self._parse(html)

        has_search = bool(
            soup.find(attrs={'role': 'search'}) or
            soup.find('input', attrs={'type': 'search'}) or
            soup.find('form', class_=lambda c: c and 'search' in str(c).lower())
        )

        nav_links = soup.find_all('nav')
        list_navs = soup.find_all(['ul', 'ol'], class_=lambda c: c and 'nav' in str(c).lower())
        total_nav_links = len(nav_links) + len(list_navs)

        has_sitemap = bool(soup.find('a', href=lambda h: h and 'sitemap' in h.lower()))

        if not has_search and total_nav_links == 0 and not has_sitemap:
            issues.append(Issue(
                name=self.name,
                criterion=self.criterion,
                level=self.level,
                element='navigation',
                line=1,
                message='На странице отсутствуют альтернативные способы навигации',
                recommendation='Добавьте поиск, навигационное меню или ссылку на карту сайта'
            ))

        return issues
from typing import List
from .base import WCAGRule, Issue


class SectionHeadingsRule(WCAGRule):
    name = "Section Headings"
    criterion = "2.4.10"
    level = "AAA"

    def check(self, html: str) -> List[Issue]:
        """
        Проверить наличие заголовков в основных секциях страницы
        """
        issues = []
        soup = self._parse(html)

        semantic_sections = soup.find_all(['article', 'section', 'aside', 'nav'])

        for section in semantic_sections:
            has_heading = section.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

            has_aria_label = section.has_attr('aria-label') and section['aria-label'].strip()
            has_aria_labelledby = section.has_attr('aria-labelledby')

            if not has_heading and not has_aria_label and not has_aria_labelledby:
                issues.append(self._issue(
                    section,
                    f'Секция <{section.name}> не содержит заголовка',
                    'Добавьте заголовок (h1-h6) или aria-label для описания секции',
                    html
                ))

        return issues

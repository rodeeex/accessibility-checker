from typing import List
from .base import WCAGRule, Issue

class LabelsOrInstructionsRule(WCAGRule):
    name: str = "Labels or Instructions"
    criterion: str = "3.3.2"
    level: str = "A"

    def _has_label(self, element, soup) -> bool:
        """Проверить, имеет ли поле ввода связанную метку"""
        element_id = element.get('id')

        if element_id:
            if soup.find('label', attrs={'for': element_id}):
                return True

        parent = element.parent
        if parent and parent.name == 'label':
            return True

        if element.get('aria-label') or element.get('aria-labelledby'):
            return True

        if element.get('title'):
            return True

        if element.get('placeholder') and element.name == 'input':
            return True

        return False

    def check(self, html: str) -> List[Issue]:
        """
        Проверяет поля формы на наличие меток или инструкций.
        """
        issues: List[Issue] = []
        soup = self._parse(html)

        form_elements = ['input', 'select', 'textarea']

        for element in soup.find_all(form_elements):
            if not self._has_label(element, soup):
                issues.append(self._issue(
                    element,
                    "Отсутствует метка или инструкция для поля ввода",
                    "Добавьте связанный элемент <label> или инструкцию для поля",
                    html
                ))

        return issues

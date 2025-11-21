from typing import List, Set
from .base import WCAGRule, Issue


class StatusMessagesRule(WCAGRule):
    name = "Status Messages"
    criterion = "4.1.3"
    level = "AA"

    STATUS_CLASSES: Set[str] = {
        'alert', 'error', 'warning', 'success', 'info', 'message',
        'notification', 'toast', 'banner', 'status'
    }

    def check(self, html: str) -> List[Issue]:
        """
        Проверить наличие ARIA-атрибутов для сообщений статуса
        """
        issues = []
        soup = self._parse(html)

        for elem in soup.find_all(class_=True):
            elem_classes = ' '.join(elem.get('class', [])).lower()

            is_status = any(status_class in elem_classes for status_class in self.STATUS_CLASSES)

            if is_status:
                has_aria = any([
                    elem.has_attr('role') and elem['role'] in ['alert', 'status', 'log'],
                    elem.has_attr('aria-live'),
                    elem.has_attr('aria-atomic')
                ])

                if not has_aria:
                    issues.append(self._issue(
                        elem,
                        f'Статусное сообщение не имеет ARIA-атрибутов',
                        'Добавьте role="alert", role="status" или aria-live="polite"',
                        html
                    ))

        return issues

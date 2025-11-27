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

    STATUS_KEYWORDS: Set[str] = {
        'ошибка', 'error', 'ошибки', 'failed', 'fail', 'сбой',
        'успех', 'success', 'успешно', 'completed', 'готово',
        'предупреждение', 'warning', 'внимание', 'alert',
        'информация', 'info', 'инфо', 'информационное сообщение'
    }

    def check(self, html: str) -> List[Issue]:
        """
        Проверить наличие ARIA-атрибутов для сообщений статуса (только листовые элементы)
        """
        issues = []
        soup = self._parse(html)

        for elem in soup.find_all(['div', 'span', 'p', 'strong', 'em', 'b', 'i', 'small', 'li']):
            if elem.find(recursive=False) is not None:
                continue

            direct_text = ''.join(s for s in elem.find_all(string=True, recursive=False)).strip()
            if not direct_text:
                continue

            direct_text_lower = direct_text.lower()

            elem_classes = ' '.join(elem.get('class', [])).lower()
            is_status_by_class = any(status_class in elem_classes for status_class in self.STATUS_CLASSES)

            is_status_by_text = any(keyword in direct_text_lower for keyword in self.STATUS_KEYWORDS)

            if not is_status_by_class and not is_status_by_text:
                continue

            has_aria = bool(
                elem.get('role') in ['alert', 'status', 'log'] or
                elem.get('aria-live') or
                elem.get('aria-atomic')
            )

            if not has_aria:
                issues.append(self._issue(
                    elem,
                    'Статусное сообщение не имеет ARIA-атрибутов',
                    'Добавьте role="alert", role="status" или aria-live="polite"',
                    html
                ))

        return issues
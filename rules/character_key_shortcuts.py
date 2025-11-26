from typing import List
from .base import WCAGRule, Issue

class CharacterKeyShortcutsRule(WCAGRule):
    name: str = "Character Key Shortcuts"
    criterion: str = "2.1.4"
    level: str = "A"

    def check(self, html: str) -> List[Issue]:
        """
        Проверяет HTML на наличие сочетаний клавиш с одиночными символами без возможности их управления.
        """
        issues: List[Issue] = []
        soup = self._parse(html)
        key_event_attrs = ['onkeydown', 'onkeypress', 'onkeyup']
      
        for element in soup.find_all(True):
            for attr in key_event_attrs:
                if element.has_attr(attr):
                    script = element[attr]
                    if self._has_single_character_shortcut(script):
                        issues.append(self._issue(
                            element,
                            f"Используется сочетание клавиш на символы через {attr} без управления",
                            "Обеспечьте возможность отключения, изменения или обхода таких сочетаний клавиш",
                            html
                        ))
        return issues

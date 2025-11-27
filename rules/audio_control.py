from typing import List
from .base import WCAGRule, Issue

class AudioControlRule(WCAGRule):
    name: str = "Audio Control"
    criterion: str = "1.4.2"
    level: str = "A"

    def check(self, html: str) -> List[Issue]:
        """
        Проверяет наличие элементов управления у аудио, которое автоматически воспроизводится.
        """
        issues: List[Issue] = []
        soup = self._parse(html)

        for audio in soup.find_all('audio'):
            autoplay = audio.has_attr('autoplay')
            controls = audio.has_attr('controls')

            if autoplay and not controls:
                issues.append(self._issue(
                    audio,
                    "Автоматически воспроизводимое аудио без элементов управления",
                    "Добавьте элементы управления (например, controls) к аудио для управления воспроизведением",
                    html
                ))

        return issues

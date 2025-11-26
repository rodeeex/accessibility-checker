from typing import List
from .base import WCAGRule, Issue

class AudioControlRule(WCAGRule):
    name = "Audio Control"
    criterion = "1.4.2"
    level = "A"

    def check(self, html: str) -> List[Issue]:
        issues = []
        soup = self._parse(html)  # Используем метод базового класса для парсинга

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

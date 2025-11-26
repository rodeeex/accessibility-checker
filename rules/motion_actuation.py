from typing import List
from .base import WCAGRule, Issue

class MotionActuationRule(WCAGRule):
    name: str = "Motion Actuation"
    criterion: str = "2.5.4"
    level: str = "A"

    def check(self, html: str) -> List[Issue]:
        """
        Проверяет HTML на наличие элементов, использующих события движения устройства,
        и отсутствие альтернативных элементов управления.
        """
        issues: List[Issue] = []
        soup = self._parse(html)

        motion_events = ['ondevicemotion', 'ondeviceorientation', 'ongesturestart', 'ongesturechange', 'ongestureend']
        for element in soup.find_all(True):
            for event in motion_events:
                if element.has_attr(event):
                    has_alternative = False
                    siblings = element.find_next_siblings()
                    for sib in siblings:
                        if sib.name == 'button' or (sib.has_attr('onclick')):
                            has_alternative = True
                            break
                    if not has_alternative:
                        issues.append(self._issue(
                            element,
                            f"Используется событие движения устройства '{event}' без альтернативного способа управления",
                            "Обеспечьте альтернативный механизм управления, не зависящий от движения устройства",
                            html
                        ))

        return issues

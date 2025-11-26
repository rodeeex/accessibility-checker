from .base import WCAGRule, Issue
from typing import List


class ChangeOnRequestRule(WCAGRule):
    name = "Change on Request"
    criterion = "3.2.5"
    level = "AAA"

    def check(self, html: str) -> List[Issue]:
        """
        Проверить отсутствие автоматических изменений контента
        """
        issues = []
        soup = self._parse(html)

        for elem in soup.find_all(["video", "audio"]):
            if elem.has_attr("autoplay"):
                issues.append(self._issue(
                    elem,
                    "Медиа запускается автоматически с помощью autoplay",
                    "Удалите autoplay или сделайте запуск по пользовательскому действию",
                    html
                ))

        for meta in soup.find_all("meta", attrs={"http-equiv": True}):
            if meta.get("http-equiv").lower() == "refresh":
                issues.append(self._issue(
                    meta,
                    "Страница автоматически обновляется через meta refresh",
                    "Удалите meta refresh, обеспечив обновление по запросу",
                    html
                ))

        for form in soup.find_all("form"):
            if form.has_attr("onchange"):
                issues.append(self._issue(
                    form,
                    "Форма отправляется автоматически при изменении",
                    "Переведите отправку формы на явное действие пользователя",
                    html
                ))

        return issues

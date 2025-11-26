from abc import ABC, abstractmethod
from typing import List, ClassVar
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class Issue:
    """
    Найденное нарушение WCAG
    """
    name: str  # Название правила
    criterion: str  # Критерий WCAG (например, "1.1.1")
    level: str  # Уровень WCAG (A, AA, AAA)
    element: str  # HTML-элемент, где обнаружена ошибка
    line: int  # Номер строки в исходном HTML-коде
    message: str  # Описание ошибки
    recommendation: str  # Рекомендация по исправлению


class WCAGRule(ABC):
    """
    Абстрактный класс для правил WCAG
    """
    name: str = ""
    criterion: str = ""
    level: str = ""

    # Список классов-наследников WCAGRule
    _registry: ClassVar[List[type["WCAGRule"]]] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.__name__ != "WCAGRule":
            WCAGRule._registry.append(cls)

    @classmethod
    def get_all_rules(cls) -> List[type["WCAGRule"]]:
        """
        Получить список всех правил WCAG
        """
        return cls._registry

    @classmethod
    def run_all(cls, html: str) -> list[Issue]:
        """
        Проверить страницу по всем зарегистрированным правилам

        :param html: HTML-контент страницы
        :return: список всех найденных нарушений
        """
        all_issues = []
        rules = cls.get_all_rules()

        for rule in rules:
            try:
                instance = rule()
                issues = instance.check(html=html)
                all_issues.extend(issues)
            except Exception as e:
                print(f"Ошибка в {rule.name}: {e}")

        return all_issues

    @abstractmethod
    def check(self, html: str) -> List[Issue]:
        """
        Проверить HTML-страницу на соответствие ОДНОМУ правилу (данный метод реализуется в наследниках)

        :param html: HTML-контент страницы
        :return: список найденных нарушений
        """
        pass

    def _parse(self, html: str) -> BeautifulSoup:
        """
        Спарсить HTML-контент

        :param html: HTML-контент
        """
        return BeautifulSoup(html, 'html.parser')

    def _get_line(self, html: str, element) -> int:
        if not element:
            return 0

        line = getattr(element, 'sourceline', None)
        if line:
            return line

        if not html:
            return 0

        candidates = []
        for attr in ('href', 'src', 'id', 'name', 'aria-label', 'title'):
            value = element.get(attr)
            if value:
                candidates.append(value)

        text = element.get_text(strip=True)
        if text and len(text) > 3:
            candidates.append(text)

        html_lower = html.lower()
        for cand in candidates:
            if cand:
                pos = html_lower.find(str(cand).lower())
                if pos != -1:
                    return html.count('\n', 0, pos) + 1

        return 0

    def _issue(self, element, message: str, recommendation: str, html: str = "") -> Issue:
        """
        Создать объект Issue для найденного нарушения

        :param element: HTML-элемент BeautifulSoup
        :param message: сообщение о нарушении
        :param recommendation: рекомендация по исправлению
        :param html: исходный HTML для определения строки
        :return: объект Issue
        """
        if hasattr(element, 'name'):
            element_str = str(element)

            if element_str.count('\n') > 50:
                attrs_parts = []
                for k, v in element.attrs.items():
                    if isinstance(v, list):
                        v = ' '.join(v)
                    v = str(v).replace('"', '&quot;')
                    attrs_parts.append(f'{k}="{v}"')

                attrs_str = ' '.join(attrs_parts)
                element_repr = f"<{element.name} {attrs_str}>..."
            else:
                element_repr = element_str
        else:
            element_repr = 'unknown'

        return Issue(
            name=self.name,
            criterion=self.criterion,
            level=self.level,
            element=element_repr,
            line=self._get_line(html, element) if html else 0,
            message=message,
            recommendation=recommendation
        )

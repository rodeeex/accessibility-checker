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
    Абстрактный класс для правил WCAG (метод check реализовывается в наследниках)
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
        :return: Список всех найденных нарушений
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
        Проверить HTML-страницу на соответствие правилу

        :param html: HTML-контент страницы
        :return: список найденных нарушений
        """
        pass

    def _parse(self, html: str) -> BeautifulSoup:
        """
        Парсинг HTML-контента

        :param html: HTML-контент
        """
        return BeautifulSoup(html, 'html.parser')

    def _get_line(self, html: str, element_str: str) -> int:
        """
        Определение номера строки элемента в исходном HTML-коде

        :param html: HTML-контент
        :param element_str: строковое представление элемента
        :return: номер строки (возвращает 0, если не получилось найти)
        """
        for i, line in enumerate(html.split('\n'), 1):
            if element_str[:50] in line:
                return i
        return 0

    def _issue(self, element, message: str, recommendation: str, html: str = "") -> Issue:
        """
        Создать объект Issue для найденного нарушения

        :param element: HTML-элемент
        :param message: Сообщение о нарушении
        :param recommendation: Рекомендация по исправлению
        :param html: Исходный HTML для определения строки
        :return: Объект Issue
        """
        element_str = str(element)
        return Issue(
            name=self.name,
            criterion=self.criterion,
            level=self.level,
            element=element.name if hasattr(element, 'name') else 'unknown',
            line=self._get_line(html, element_str) if html else 0,
            message=message,
            recommendation=recommendation
        )

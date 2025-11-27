# Accessibility Checker

CLI-утилита для быстрой проверки веб-страниц на соответствие базовым критериям доступности (согласно WCAG 2.1)

---

## Как запустить? (Windows)

1. Скачайте последний [релиз](https://github.com/rodeeex/accessibility-checker/releases)

2. Запустите в PowerShell или CMD:

```bash
# Проверить и вывести в консоль
.\accessibility-checker.exe https://example.com

# Сохранить HTML-отчёт
.\accessibility-checker.exe https://example.com --report html --filename report.html

# Сохранить JSON-отчёт
.\accessibility-checker.exe https://example.com --report json --filename report.json
```

| Флаг         | Краткая форма | Тип                           | По умолчанию          | Описание                                                         |
|--------------|---------------|-------------------------------|-----------------------|------------------------------------------------------------------|
| `--report`   | `-r`          | `console` \| `html` \| `json` | `console`             | Формат вывода отчёта                                             |
| `--filename` | `-f`          | путь к файлу                  | название генерируется | Сохранить отчёт в указанный файл в папке ./accessibility_reports |
| `--timeout`  | `-t`          | целое (секунды)               | `30`                  | Максимальное время ожидания загрузки страницы                    |



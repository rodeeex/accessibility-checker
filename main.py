"""
Чекер доступности веб-сайтов
CLI инструмент для проверки доступности веб-страниц с использованием Playwright
"""

import argparse
import sys
from urllib.parse import urlparse
from browser.fetcher import fetch_page
from report_maker import make_report, save_report_to_file, get_reports_directory
from rules import WCAGRule


def validate_url(url: str) -> bool:
    """Валидация URL"""
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False
        if result.scheme not in ('http', 'https'):
            return False
        return True
    except Exception:
        return False


def parse_arguments():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description='Чекер доступности веб-сайтов',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры использования:
python main.py https://example.com
python main.py https://example.com --report json --timeout 30
python main.py https://example.com --report json --filename report.json
python main.py https://example.com --report html --filename accessibility_report.html
        '''
    )

    parser.add_argument(
        'url',
        help='URL веб-сайта для проверки доступности'
    )

    parser.add_argument(
        '-r', '--report',
        choices=['json', 'html', 'console'],
        default='console',
        help='Формат вывода отчёта (по умолчанию: console)'
    )

    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=30,
        metavar='N',
        help='Таймаут загрузки в секундах (по умолчанию: 30)'
    )

    parser.add_argument(
        '-f', '--filename',
        dest='filename',
        type=str,
        metavar='FILE',
        help='Файл для сохранения отчёта (для json/html)'
    )

    return parser.parse_args()


def main():
    """Основная функция"""
    try:
        args = parse_arguments()

        if not validate_url(args.url):
            print(f"Ошибка: Некорректный URL '{args.url}'", file=sys.stderr)
            print("URL должен начинаться с http:// или https://", file=sys.stderr)
            sys.exit(1)

        if args.timeout <= 0:
            print(f"Ошибка: Таймаут должен быть положительным числом, получено: {args.timeout}", file=sys.stderr)
            sys.exit(1)

        if args.filename and args.report == 'console':
            print("Предупреждение: Аргумент --filename игнорируется при формате отчета 'console'", file=sys.stderr)

        print(f"\nПроверка: {args.url}")
        print(f"Формат: {args.report} | Таймаут: {args.timeout}s\n")

        # Загрузка страницы
        try:
            page_data = fetch_page(args.url, args.timeout)
            print(f"✓ Загружено: {page_data['title']} ({page_data['status']})")
        except Exception as e:
            print(f"✗ Ошибка загрузки: {e}", file=sys.stderr)
            sys.exit(1)

        # Проверка правил WCAG
        try:
            issues = WCAGRule.run_all(page_data['html'])
            print(f"✓ Найдено проблем: {len(issues)}\n")
        except Exception as e:
            print(f"✗ Ошибка проверки: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            sys.exit(1)

        # Генерация отчёта
        try:
            if args.report == 'console':
                report_content = make_report(issues, page_data['url'], 'console')
                print(report_content)
            else:
                if args.filename:
                    file_path = save_report_to_file(
                        issues, page_data['url'], args.report,
                        filename=args.filename
                    )
                else:
                    reports_dir = get_reports_directory()
                    file_path = save_report_to_file(
                        issues, page_data['url'], args.report,
                        output_path=reports_dir
                    )

                print(f"✓ Отчёт сохранён: {file_path}\n")

        except Exception as e:
            print(f"✗ Ошибка при создании отчёта: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            sys.exit(1)

        sys.exit(0 if len(issues) == 0 else 1)

    except KeyboardInterrupt:
        print("\n\n⚠ Проверка прервана пользователем", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Неожиданная ошибка: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
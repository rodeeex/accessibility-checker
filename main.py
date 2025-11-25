#!/usr/bin/env python3
"""
Чекер доступности веб-сайтов
CLI инструмент для проверки доступности веб-страниц с использованием Playwright
"""

import argparse
import sys
from urllib.parse import urlparse
from report_maker import make_report, save_report_to_file, get_reports_directory


def validate_url(url):
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
  python main.py https://example.com --report pdf --timeout 60
  python main.py https://example.com --report json --filename report.json
  python main.py https://example.com --report html --filename accessibility_report.html
        '''
    )

    parser.add_argument(
        'url',
        help='URL веб-сайта для проверки доступности'
    )

    parser.add_argument(
        '--report',
        choices=['json', 'pdf', 'html', 'console'],
        default='console',
        help='Формат вывода отчета (по умолчанию: console)'
    )

    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        metavar='N',
        help='Таймаут в секундах (по умолчанию: 30)'
    )

    parser.add_argument(
        '--filename',
        type=str,
        metavar='FILE',
        help='Имя файла для сохранения отчета (используется с форматами json, pdf, html)'
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

        print(f"URL для проверки: {args.url}")
        print(f"Формат отчета: {args.report}")
        print(f"Таймаут: {args.timeout} секунд")
        if args.filename and args.report != 'console':
            print(f"Файл отчета: {args.filename}")

        # TODO: Здесь будет реализована логика проверки доступности с Playwright
        print("\nНачинаю проверку доступности...")

        # Заглушка - список найденных проблем (в будущем будет заменен на реальную проверку)
        issues = []  # Пока пустой список, в будущем здесь будут реальные проблемы

        # Обработка результатов
        if args.report == 'console':
            report_content = make_report(issues, args.url, 'console')
            print(report_content)
        else:
            try:
                if args.filename:
                    file_path = save_report_to_file(
                        issues, args.url, args.report,
                        filename=args.filename
                    )
                else:
                    reports_dir = get_reports_directory()
                    file_path = save_report_to_file(
                        issues, args.url, args.report,
                        output_path=reports_dir
                    )

                print(f"\nОтчет сохранен: {file_path}")

            except Exception as e:
                print(f"\nОшибка при сохранении отчета: {e}", file=sys.stderr)
                sys.exit(1)

    except KeyboardInterrupt:
        print("\nПроверка прервана пользователем", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

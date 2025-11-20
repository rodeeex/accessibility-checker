#!/usr/bin/env python3
"""
Чекер доступности веб-сайтов
CLI инструмент для проверки доступности веб-страниц с использованием Playwright
"""

import argparse
import sys
from urllib.parse import urlparse


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

    # Позиционный аргумент для URL
    parser.add_argument(
        'url',
        help='URL веб-сайта для проверки доступности'
    )

    # Аргумент для формата отчета
    parser.add_argument(
        '--report',
        choices=['json', 'pdf', 'html', 'console'],
        default='console',
        help='Формат вывода отчета (по умолчанию: console)'
    )

    # Аргумент для таймаута
    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        metavar='N',
        help='Таймаут в секундах (по умолчанию: 30)'
    )

    # Аргумент для имени файла отчета
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

        # Валидация URL
        if not validate_url(args.url):
            print(f"Ошибка: Некорректный URL '{args.url}'", file=sys.stderr)
            print("URL должен начинаться с http:// или https://", file=sys.stderr)
            sys.exit(1)

        # Валидация таймаута
        if args.timeout <= 0:
            print(f"Ошибка: Таймаут должен быть положительным числом, получено: {args.timeout}", file=sys.stderr)
            sys.exit(1)

        # Валидация filename
        if args.filename and args.report == 'console':
            print("Предупреждение: Аргумент --filename игнорируется при формате отчета 'console'", file=sys.stderr)

        # Вывод параметров для проверки
        print(f"URL для проверки: {args.url}")
        print(f"Формат отчета: {args.report}")
        print(f"Таймаут: {args.timeout} секунд")
        if args.filename and args.report != 'console':
            print(f"Файл отчета: {args.filename}")

        # TODO: Здесь будет реализована логика проверки доступности с Playwright
        print("\nНачинаю проверку доступности...")

    except KeyboardInterrupt:
        print("\nПроверка прервана пользователем", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

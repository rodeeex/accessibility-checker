import asyncio
from typing import Dict
from playwright.async_api import TimeoutError as PlaywrightTimeout, ViewportSize
from playwright_stealth import Stealth
from playwright.async_api import async_playwright

from browser.exceptions import PageFetchTimeout, PageFetchError


class PageFetcher:
    def __init__(self, timeout: int = 30000):
        """
        :param timeout: интервал ожидания в мс
        """
        self.timeout = timeout

    async def fetch(self, url: str) -> Dict[str, any]:
        """
        Загружает страницу и возвращает данные

        :param url: адрес страницы
        :return: словарь с ключами html, url, title, status
        """
        try:
            # Запуск в stealth-режиме для обхода блокировок ботов
            stealth = Stealth()

            async with stealth.use_async(async_playwright()) as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--disable-dev-shm-usage",
                        "--no-sandbox",
                    ],
                )

                context = await browser.new_context(
                    viewport=ViewportSize(width=1920, height=1080),
                    user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
                    ),
                    locale="ru-RU",
                )

                await stealth.apply_stealth_async(context)

                page = await context.new_page()
                page.set_default_timeout(self.timeout)

                response = await page.goto(url, wait_until="networkidle")
                await page.wait_for_load_state("domcontentloaded")

                html_content = await page.content()
                final_url = page.url
                title = await page.title()
                status = response.status if response else None

                await browser.close()

                return {
                    "html": html_content,
                    "url": final_url,
                    "title": title,
                    "status": status,
                }

        except PlaywrightTimeout:
            raise PageFetchTimeout(url, self.timeout)

        except Exception as e:
            raise PageFetchError(url, e)


def fetch_page(url: str, timeout: int = 30) -> Dict[str, any]:
    """
    Синхронная обёртка вокруг fetch

    :param url: адрес страницы
    :param timeout: интервал ожидания в секундах
    :return: словарь с ключами html, url, title, status
    """
    fetcher = PageFetcher(timeout * 1000)
    return asyncio.run(fetcher.fetch(url))

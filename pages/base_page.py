from playwright.sync_api import Page, Locator, expect
from typing import Optional


class BasePage:
    """
    базовый класс для всех page objects с общими методами 
    """
    
    def __init__(self, page: Page):
        """
        инициализация базовой страницы
        """
        self.page = page
    
    def navigate(self, url: str):
        """
        переход на указанный URL        
        """
        self.page.goto(url)
    
    def get_current_url(self) -> str:
        """
        получение текущего URL страницы
        returns:
            текущий URL (str)
        """
        return self.page.url
    
    def wait_for_url(self, url_pattern: str, timeout: int = 30000):
        """
        ожидание перехода на URL содержащий указанный паттерн
        """
        self.page.wait_for_url(f"*{url_pattern}*", timeout=timeout)
    
    def click(self, locator: str, timeout: int = 30000):
        """
        клик по locator
        """
        self.page.locator(locator).click(timeout=timeout)
    
    def fill(self, locator: str, value: str, timeout: int = 30000):
        """
        заполнение поля ввода
        """
        self.page.locator(locator).fill(value, timeout=timeout)
    
    def get_text(self, locator: str, timeout: int = 30000) -> str:
        """
        получение текста элемента
        returns:
            Текст элемента (str)
        """
        return self.page.locator(locator).inner_text(timeout=timeout)
    
    def is_visible(self, locator: str, timeout: int = 5000) -> bool:
        """
        проверка видимости элемена    
        returns:
            true если видно, false если нет (bool)
        """
        try:
            self.page.locator(locator).wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False
    
    def wait_for_element(self, locator: str, timeout: int = 30000) -> Locator:
        """
        ожидание появления элемента.
        returns:
            Locator элемента
        """
        return self.page.locator(locator).wait_for(state="visible", timeout=timeout)
    
    def select_option(self, locator: str, value: str, timeout: int = 30000):
        """
        выбор опции в селекторе
        """
        self.page.locator(locator).select_option(value, timeout=timeout)
    
    def wait_for_selector(self, selector: str, timeout: int = 30000):
        """
        ожидание появления селектора
        """
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def take_screenshot(self, path: str) -> None:
        """
        сфоткаться(скриншот)
        """
        self.page.screenshot(path=path)
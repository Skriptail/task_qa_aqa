"""
pytest конфигурация и фикстуры для e2e тестов
"""
import pytest
from playwright.sync_api import Page, Browser, BrowserContext
from pages.payment_page import PaymentPage
from pages.payment_processing_page import PaymentProcessingPage
from utils.test_data import PAYMENT_CREATE_URL, PAYMENT_CREATE_URL_WITH_PROMO


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """
    настройки запуска браузера.
    можно добавить опции для headless режима размеров окна и слоумо
    """
    return {
        "headless": True, 
        "slow_mo": 0, 
    }


@pytest.fixture(scope="session")
def browser_context_args():
    """
    настройки контекста браузера.
    """
    return {
        "viewport": {"width": 1920, "height": 1080},
        "locale": "ru-RU",
    }


@pytest.fixture(scope="function")
def payment_page(page: Page) -> PaymentPage:
    """    
    returns:
        PaymentPage: объект страницы создания заказа
    """
    return PaymentPage(page)


@pytest.fixture(scope="function")
def payment_processing_page(page: Page) -> PaymentProcessingPage:
    """
    returns:
        PaymentProcessingPage: объект страницы оплаты
    """
    return PaymentProcessingPage(page)


@pytest.fixture(scope="function")
def payment_page_with_promo(page: Page) -> PaymentPage:
    """
    returns:
        PaymentPage: объект страницы создания заказа
    """
    payment_page = PaymentPage(page)
    payment_page.navigate(PAYMENT_CREATE_URL_WITH_PROMO)
    return payment_page


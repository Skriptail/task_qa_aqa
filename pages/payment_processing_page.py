from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.test_data import THANK_YOU_URL_PATTERN


class PaymentProcessingPage(BasePage):
    """
    page object для ввода реквизитов карты
    открывается после выбора способа оплаты
    """
    
    # локаторы формы карты
    CARD_NUMBER_INPUT = "#cardNumber"
    CARD_EXPIRY_INPUT = "#expDateMonthYear"
    CARD_CVV_INPUT = "#cvv"
    
    # локатор кнопки оплаты
    SUBMIT_BUTTON = "#pay-btn"
    
    def __init__(self, page: Page):
        """
        инициализация страницы оплаты
        """
        super().__init__(page)
    
    def fill_card_data(self, card_number: str, card_expiry: str, card_cvv: str) -> None:
        """
        заполнение данных карты для оплаты
        """
        # номер карты
        self.wait_for_element(self.CARD_NUMBER_INPUT)
        self.fill(self.CARD_NUMBER_INPUT, card_number)
        
        # срок действия
        self.wait_for_element(self.CARD_EXPIRY_INPUT)
        self.fill(self.CARD_EXPIRY_INPUT, card_expiry)
        
        # CVV
        self.wait_for_element(self.CARD_CVV_INPUT)
        self.fill(self.CARD_CVV_INPUT, card_cvv)
    
    # локаторы кнопок на странице 3DS
    SUCCESS_BUTTON_3DS = ".button_primary > div:nth-child(1)"
    NEGATIVE_BUTTON_3DS = ".button_secondary > div:nth-child(1)"
    
    def submit_payment(self) -> None:
        """
        отправка формы оплаты
        после отправки редирект на страницу 3DS
        """
        self.wait_for_element(self.SUBMIT_BUTTON)
        self.click(self.SUBMIT_BUTTON)
    
    def wait_for_payment_processing(self, timeout: int = 60000) -> None:
        """
        ожидание обработки оплаты и перехода на страницу спасибо
        после submit_payment редирект на 3DS, нажимаем кнопку успех, редирект на спасибо
        """
        # ждем появления страницы 3DS
        self.page.wait_for_url("**acs.cloudpayments.ru**", timeout=30000)
        
        # ждем загрузки страницы
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        # нажимаем кнопку "Успех" на странице 3DS
        self.wait_for_element(self.SUCCESS_BUTTON_3DS)
        # ожидаем навигацию на страницу "Спасибо" после клика
        with self.page.expect_navigation(timeout=timeout, url=f"**{THANK_YOU_URL_PATTERN}**"):
            self.click(self.SUCCESS_BUTTON_3DS)
    
    def wait_for_payment_error(self, timeout: int = 60000) -> None:
        """
        ожидание обработки оплаты с ошибкой (недостаток средств)
        после submit_payment редирект на 3DS, нажимаем кнопку для ошибки, редирект на /fail
        """
        # ждем появления страницы 3DS
        self.page.wait_for_url("**acs.cloudpayments.ru**", timeout=30000)
        self.page.wait_for_load_state("networkidle", timeout=10000)
        self.wait_for_element(self.NEGATIVE_BUTTON_3DS)
        # ожидамем навигацию на страницу /fail после клика
        with self.page.expect_navigation(timeout=timeout, url="**/fail**"):
            self.click(self.NEGATIVE_BUTTON_3DS)
        
        # ждем появления блока с ошибкой на странице /fail
        self.wait_for_element(".alert", timeout=10000)
    
    def is_error_message_visible(self) -> bool:
        """
        проверка наличия сообщения об ошибке на странице
        """
        error_selector = ".alert"
        return self.is_visible(error_selector, timeout=5000)
    
    def get_error_message(self) -> str:
        """
        получение текста сообщения об ошибке
        """
        error_selector = ".alert"                    
        if self.is_visible(error_selector, timeout=2000):
            return self.get_text(error_selector)
        
        return ""
    
    def is_card_form_visible(self) -> bool:
        """
        проверка видимости формы ввода данных карты
        """
        return self.is_visible(self.CARD_NUMBER_INPUT) and self.is_visible(self.CARD_EXPIRY_INPUT)


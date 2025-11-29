from playwright.sync_api import Page
from pages.base_page import BasePage


class PaymentPage(BasePage):
    """
    page object для страницы создания заказа
    методы для работы с формой заказа
    """
    
    # локаторы формы заказа
    NAME_INPUT = "#name"
    EMAIL_INPUT = "#email"
    PHONE_INPUT = "#phone"
    PROMOCODE_INPUT = "#promocode"
    PROMOCODE_BUTTON = ".co-promocode-button"
    
    # локатор выбора российских карт
    # после клика редирект на страницу ввода реквизитов карты
    PAYMENT_TYPE_RUSSIAN = "#russian-cards-button"
    
    def __init__(self, page: Page):
        """
        инициализация страницы оплаты
        """
        super().__init__(page)
    
    def fill_customer_info(self, name: str, email: str, phone: str):
        """
        заполнение информации о клиенте (имя, email, телефон)
        """
        # заполнение имени
        # используем явное ожидание wait_for_element
        self.wait_for_element(self.NAME_INPUT)
        self.fill(self.NAME_INPUT, name)
        
        # заполнение email
        self.wait_for_element(self.EMAIL_INPUT)
        self.fill(self.EMAIL_INPUT, email)
        
        # заполнение телефона
        self.wait_for_element(self.PHONE_INPUT)
        self.fill(self.PHONE_INPUT, phone)
    
    def apply_promocode(self, promocode: str):
        """
        применение промокода.
        """
        # проверяем что поле промокода видно
        if self.is_visible(self.PROMOCODE_INPUT):
            self.fill(self.PROMOCODE_INPUT, promocode)
            # пытаемся найти и нажать кнопку применения промокода
            if self.is_visible(self.PROMOCODE_BUTTON):
                self.click(self.PROMOCODE_BUTTON)
            else:
                raise ValueError(f"Кнопка применения промокода не найдена: {self.PROMOCODE_BUTTON}")
    
    def select_russian_cards(self):
        """
        выбор российских карт для оплаты
        после клика редирект на страницу ввода реквизитов карты
        """
        self.wait_for_element(self.PAYMENT_TYPE_RUSSIAN)
        # ожидаем навигацию на страницу ввода реквизитов карты
        with self.page.expect_navigation(timeout=30000):
            self.click(self.PAYMENT_TYPE_RUSSIAN)
    
    def is_payment_form_visible(self) -> bool:
        """
        проверка видимости формы оплаты
        """
        return self.is_visible(self.NAME_INPUT) and self.is_visible(self.EMAIL_INPUT)
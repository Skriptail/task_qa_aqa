"""
негативные тесты создания заказа и оплаты
"""
import pytest
from utils.test_data import (
    PAYMENT_CREATE_URL_WITH_PROMO,
    VALID_USER,
    INSUFFICIENT_FUNDS_CARD,
    TEST_PROMOCODE
)


@pytest.mark.negative
def test_payment_with_insufficient_funds(
    payment_page_with_promo,
    payment_processing_page
):
    """
    негативный тест: оплата с недостатком средств на карте
    """
    # страница уже открыта через фикстуру
    # проверяем что форма видима
    assert payment_page_with_promo.is_payment_form_visible(), \
        "Форма создания заказа не отображается"
    
    # заполняем информацию о клиенте
    payment_page_with_promo.fill_customer_info(
        name=VALID_USER.name,
        email=VALID_USER.email,
        phone=VALID_USER.phone
    )
    
    # применяем промокод
    payment_page_with_promo.apply_promocode(TEST_PROMOCODE)
    
    # выбираем способ оплаты (российские карты)
    payment_page_with_promo.select_russian_cards()
    
    # проверяем что мы на странице ввода реквизитов карты
    assert payment_processing_page.is_card_form_visible(), \
        "Форма ввода данных карты не отображается"
    
    # заполняем данные карты с недостатком средств
    payment_processing_page.fill_card_data(
        card_number=INSUFFICIENT_FUNDS_CARD.number,
        card_expiry=INSUFFICIENT_FUNDS_CARD.expiry,
        card_cvv=INSUFFICIENT_FUNDS_CARD.cvv
    )
    
    # отправляем форму оплаты
    payment_processing_page.submit_payment()
    
    # ожидаем обработку ошибки и редирект на страницу /fail
    payment_processing_page.wait_for_payment_error(timeout=60000)
    
    # проверяем что мы на странице ошибки
    current_url = payment_processing_page.get_current_url()
    assert "/fail" in current_url, \
        f"Не произошел переход на страницу ошибки. Текущий URL: {current_url}"
    
    # проверяем наличие сообщения об ошибке
    assert payment_processing_page.is_error_message_visible(), \
        "Сообщение об ошибке не отображается"
    
    # получаем и проверяем текст ошибки
    error_message = payment_processing_page.get_error_message()
    assert error_message, "Текст сообщения об ошибке пустой"
    print(f"Сообщение об ошибке: {error_message}")


@pytest.mark.negative
def test_payment_with_insufficient_funds_without_promocode(
    payment_page,
    payment_processing_page
):
    """
    негативный тест: оплата с недостатком средств без промокода
    """
    from utils.test_data import PAYMENT_CREATE_URL
    
    # открываем страницу оплаты
    payment_page.navigate(PAYMENT_CREATE_URL)
    
    # проверяем что форма видима
    assert payment_page.is_payment_form_visible(), \
        "Форма создания заказа не отображается"
    
    # заполняем информацию о клиенте
    payment_page.fill_customer_info(
        name=VALID_USER.name,
        email=VALID_USER.email,
        phone=VALID_USER.phone
    )
    
    # выбираем способ оплаты (российские карты)
    payment_page.select_russian_cards()
    
    # проверяем что мы на странице ввода реквизитов карты
    assert payment_processing_page.is_card_form_visible(), \
        "Форма ввода данных карты не отображается"
    
    # заполняем данные карты с недостатком средств
    payment_processing_page.fill_card_data(
        card_number=INSUFFICIENT_FUNDS_CARD.number,
        card_expiry=INSUFFICIENT_FUNDS_CARD.expiry,
        card_cvv=INSUFFICIENT_FUNDS_CARD.cvv
    )
    
    # отправляем форму оплаты
    payment_processing_page.submit_payment()
    
    # ожидаем обработку ошибки и редирект на страницу /fail
    payment_processing_page.wait_for_payment_error(timeout=60000)
    
    # проверяем что мы на странице ошибки
    current_url = payment_processing_page.get_current_url()
    assert "/fail" in current_url, \
        f"Не произошел переход на страницу ошибки. Текущий URL: {current_url}"
    
    # проверяем наличие сообщения об ошибке
    assert payment_processing_page.is_error_message_visible(), \
        "Сообщение об ошибке не отображается"
    
    # получаем и проверяем текст ошибки
    error_message = payment_processing_page.get_error_message()
    assert error_message, "Текст сообщения об ошибке пустой"
    print(f"Сообщение об ошибке: {error_message}")


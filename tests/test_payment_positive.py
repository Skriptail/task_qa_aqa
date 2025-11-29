"""
позитивные тесты создания заказа и оплаты
"""
import pytest
from utils.test_data import (
    PAYMENT_CREATE_URL_WITH_PROMO,
    SUCCESS_CARD,
    TEST_PROMOCODE,
    generate_random_user
)


@pytest.mark.positive
def test_successful_payment_with_promocode(
    payment_page_with_promo,
    payment_processing_page
):
    """
    позитивный тест: успешная оплата с промокодом
    """
    # страница уже открыта через фикстуру
    # проверяем что форма видима
    assert payment_page_with_promo.is_payment_form_visible(), \
        "Форма создания заказа не отображается"
    
    # генерируем случайные валидные данные пользователя
    random_user = generate_random_user()
    
    # заполняем информацию о клиенте
    payment_page_with_promo.fill_customer_info(
        name=random_user.name,
        email=random_user.email,
        phone=random_user.phone
    )
    
    # применяем промокод
    payment_page_with_promo.apply_promocode(TEST_PROMOCODE)
    
    # выбираем способ оплаты (российские карты)
    payment_page_with_promo.select_russian_cards()
    
    # проверяем что мы на странице ввода реквизитов карты
    assert payment_processing_page.is_card_form_visible(), \
        "Форма ввода данных карты не отображается"
    
    # заполняем данные карты
    payment_processing_page.fill_card_data(
        card_number=SUCCESS_CARD.number,
        card_expiry=SUCCESS_CARD.expiry,
        card_cvv=SUCCESS_CARD.cvv
    )
    
    # отправляем форму оплаты
    payment_processing_page.submit_payment()
    
    # проверяем переход на страницу спасибо
    payment_processing_page.wait_for_payment_processing(timeout=60000)
    
    # дополнительная проверка URL
    current_url = payment_processing_page.get_current_url()
    assert "thankyou_mid" in current_url, \
        f"Не произошел переход на страницу спасибо. Текущий URL: {current_url}"


@pytest.mark.positive
def test_successful_payment_without_promocode(
    payment_page,
    payment_processing_page
):
    """
    позитивный тест: успешная оплата без промокода
    """
    from utils.test_data import PAYMENT_CREATE_URL
    
    # открываем страницу оплаты
    payment_page.navigate(PAYMENT_CREATE_URL)
    
    # проверяем что форма видима
    assert payment_page.is_payment_form_visible(), \
        "Форма создания заказа не отображается"
    
    # генерируем случайные валидные данные пользователя
    random_user = generate_random_user()
    
    # заполняем информацию о клиенте
    payment_page.fill_customer_info(
        name=random_user.name,
        email=random_user.email,
        phone=random_user.phone
    )
    
    # выбираем способ оплаты (российские карты)
    payment_page.select_russian_cards()
    
    # проверяем что мы на странице ввода реквизитов карты
    assert payment_processing_page.is_card_form_visible(), \
        "Форма ввода данных карты не отображается"
    
    # заполняем данные карты
    payment_processing_page.fill_card_data(
        card_number=SUCCESS_CARD.number,
        card_expiry=SUCCESS_CARD.expiry,
        card_cvv=SUCCESS_CARD.cvv
    )
    
    # отправляем форму оплаты
    payment_processing_page.submit_payment()
    
    # проверяем переход на страницу спасибо
    payment_processing_page.wait_for_payment_processing(timeout=60000)
    
    # дополнительная проверка URL
    current_url = payment_processing_page.get_current_url()
    assert "thankyou_mid" in current_url, \
        f"Не произошел переход на страницу спасибо. Текущий URL: {current_url}"


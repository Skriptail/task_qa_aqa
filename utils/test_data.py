"""
тестовые данные для e2e тестов оплаты
константы для url, промокодов, тестовых карт и пользовательских данных
"""

from dataclasses import dataclass
from typing import Optional
import random
from faker import Faker

# инициализация faker для генерации случайных данных
fake = Faker('ru_RU')


# url для тестирования
BASE_URL = "https://dev.anysports.tv"
PAYMENT_CREATE_URL = f"{BASE_URL}/v2/ru/payment/create/677"
PAYMENT_CREATE_URL_WITH_PROMO = f"{PAYMENT_CREATE_URL}?p=1"  # с промокодом

# паттерны url для проверки редиректов
PAYMENT_CHECKOUT_URL_PATTERN = "/ru/payment/cloudpayments/checkout/"
THANK_YOU_URL_PATTERN = "thankyou_mid"

# промокод для тестов
TEST_PROMOCODE = "qa"

# классы для хранения данных
@dataclass
class TestUser:
    name: str
    email: str
    phone: str


@dataclass
class TestCard:
    number: str
    expiry: str 
    cvv: str
    description: str  # (для логирования)


class TestData:    
    # позитивные данные пользователя
    VALID_USER = TestUser(
        name="Тест Юзер",
        email="tetss@example.com",
        phone="+79991234567"
    )
    # успешная оплата
    SUCCESS_CARD = TestCard(
        number="5555555555554444", 
        expiry="12/27",
        cvv="123",
        description="успешная оплата (MasterCard)"
    )
    
    # альтернативная успешная карта
    SUCCESS_CARD_VISA = TestCard(
        number="4000000000003055",
        expiry="12/28",
        cvv="123",
        description="успешная оплата (Visa)"
    )
    
    # негативные сценарии
    INSUFFICIENT_FUNDS_CARD = TestCard(
        number="4012888888881881",
        expiry="12/26",
        cvv="123",
        description="недостаточно средств на карте"
    )


#алиасы 
VALID_USER = TestData.VALID_USER
SUCCESS_CARD = TestData.SUCCESS_CARD
INSUFFICIENT_FUNDS_CARD = TestData.INSUFFICIENT_FUNDS_CARD


def generate_random_user() -> TestUser:
    """
    генератор случайных валидных данных пользователя для позитивных тестов
    
    returns:
        TestUser: объект со случайными валидными данными пользователя
    """
    name = f"{fake.first_name()} {fake.last_name()}"
    email = fake.email()
    remaining_digits = ''.join(random.choices("0123456789", k=9))
    raw_phone = f"9{remaining_digits}"
    phone = f"+7 {raw_phone[:3]} {raw_phone[3:6]}-{raw_phone[6:8]}-{raw_phone[8:10]}"
    
    return TestUser(
        name=name,
        email=email,
        phone=phone
    )


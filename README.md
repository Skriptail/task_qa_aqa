E2E тесты для создания заказа и оплаты через веб-интерфей с легко мастшабируемой архитектурой
позитивные тесты используют случайные валидные данные пользователя (генерируются при каждом запуске теста и отчищались бы сразу из бд если бы был доступ)
негативные тесты используют фиксированные данные и тестовую карту с недостатком средств

тесты завернуты в докер и готовы для встраивания в пайплайн, останется встроить переменные окружения и написать .gitlab-ci.yml
## технологии
- Python 3.11
- pytest
- Playwright
- Docker Docker Compose
### быстрый старт

1. **собрать образ и запустить все тесты:**
```bash
docker-compose up --build
```

2. **только позитивные тесты:**
```bash
docker-compose run --rm tests pytest tests/test_payment_positive.py -v
```

3. **только негативные тесты:**
```bash
docker-compose run --rm tests pytest tests/test_payment_negative.py -v
```

4. **конкретный тест:**
```bash
docker-compose run --rm tests pytest tests/test_payment_positive.py::test_successful_payment_with_promocode -v
```

5. **запуск с маркерами:**
```bash
docker-compose run --rm tests pytest -m positive -v
docker-compose run --rm tests pytest -m negative -v
```

6. **с HTML отчетом:**
```bash
docker-compose run --rm tests pytest -v --html=reports/report.html --self-contained-html
```

отчет будет доступен в папке `reports/report.html`
настройки браузера можно изменить в `conftest.py`:
- `headless`: False (браузер видимый для отладки)
- `slow_mo`: 1000 (замедление действий для детального просмотра )


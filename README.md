# servers-com-tests

## RU

### О проекте

Проект содержит автоматизированные UI-тесты для платформы Servers.com на стеке **Python + Pytest + Playwright (sync API) + Allure**.

Тесты организованы по Page Object паттерну, а часть операций выполняется через API-запросы (например, авторизация и подготовка данных) для ускорения и стабилизации сценариев.

### Коротко о структуре

```text
servers-com-tests/
├── conftest.py                 # Общие фикстуры, логирование, random_user
├── pytest.ini                  # Базовые опции pytest и директория allure-results
├── requirements.txt            # Зависимости проекта
├── src/
│   ├── pages/                  # Page Objects
│   ├── models/                 # Pydantic/доменные модели
│   ├── utils/                  # Вспомогательные утилиты (config loader, logger и т.д.)
│   ├── elements/               # UI-элементы/компоненты
│   └── clients/                # Зарезервировано под API-клиенты (сейчас фактически пусто)
└── tests/
    ├── web/                    # Основные UI-тесты
    ├── test_data/              # Тестовые данные (например, users.json)
    └── api/                    # Зарезервировано под API-тесты (сейчас фактически пусто)
```

> Примечание по архитектуре:
> - `tests/api` присутствует в проекте, чтобы явно отразить будущий слой API-тестов. Сейчас директория функционально пустая (есть только технический `__init__.py`).
> - `src/clients` присутствует для будущих API-клиентов/оберток, сейчас директория пустая.

### Подробный запуск тестов

#### 1) Подготовить окружение

macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install allure-pytest
python -m playwright install chromium
```

Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install allure-pytest
python -m playwright install --with-deps chromium
```

#### 2) Подготовить тестовые данные

Файл с пользователями: `tests/test_data/users.json`.

Это файл-заглушка: перед запуском тестов впишите в него актуальные `email` и `password`.

Фикстура `random_user` берет случайного пользователя из этого файла. Если пользователь один, фактически всегда будет использоваться он.

#### 3) (Опционально) задать URL окружения

По умолчанию используется `https://portal.servers.com`.

Если нужно другое окружение:

```bash
export WEB_BASE_URL="https://your-env.example.com"
```

#### 4) Запустить все тесты

```bash
pytest
```

#### 5) Запустить отдельные наборы тестов

```bash
pytest tests/web/login
pytest tests/web/platform
pytest tests/web/platform/test_navigation.py -k submenu -v
```

#### 6) Запустить с прокси (если требуется)

В проекте есть опция `--proxy`:

```bash
pytest --proxy
pytest --proxy="socks5://127.0.0.1:9050"
```

### Генерация Allure report

`pytest.ini` уже настроен на запись результатов в `allure-results`.

#### 1) Сгенерировать результаты

```bash
pytest
```

#### 2) Убедиться, что установлен Allure CLI

macOS (Homebrew):

```bash
brew install allure
```

Linux (npm):

```bash
npm install -g allure-commandline
```

#### 3) Открыть интерактивный отчет

```bash
allure serve allure-results
```

#### 4) Сгенерировать статический отчет

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## Ограничения

- В текущей реализации покрыты в основном **позитивные сценарии**.

- Практически сразу после начала автоматизированных прогонов на платформу мой IP был заблокирован, поэтому для стабильного запуска тестов было принято решение использовать прокси.

- Сохранена возможность запуска тестов на **Firefox** и **WebKit**, но эти прогоны не проверялись, т.к. тестовый пользователь всего 1 и тесты писались, отлаживались и запускались через tor socks, что значительно влияло на время загрузки страниц, а следовательно на время выполнения тестов.

- Также проект использует **`playwright.sync_api`**, потому что в распоряжении был только один тестовый пользователь, и без полного понимания особенностей тестовой среды дополнительные пользователи не создавались.

- Запуск тестов в параллель не реализован из-за наличия ограницений выше + качественная реализация с сохранением изоляции тестов значительно бы увеличило время выполнения тестового задание. 

 Тем не менее, хочу отметить, что с удовольствием расскажу о вариантах решения этих проблем и о том, как я бы реализовал более масштабируемый фреймворк для тестирования платформы, если бы не было ограничений по времени и ресурсам.




---

## EN

### About the Project

This repository contains automated UI tests for the Servers.com platform using **Python + Pytest + Playwright (sync API) + Allure**.

Tests follow the Page Object pattern, and some operations are done via API requests (for example, login and test data setup) to improve stability and execution speed.

### Project Structure (Short)

```text
servers-com-tests/
├── conftest.py                 # Shared fixtures, logging, random_user
├── pytest.ini                  # Base pytest options and allure-results directory
├── requirements.txt            # Project dependencies
├── src/
│   ├── pages/                  # Page Objects
│   ├── models/                 # Pydantic/domain models
│   ├── utils/                  # Helper utilities (config loader, logger, etc.)
│   ├── elements/               # UI elements/components
│   └── clients/                # Reserved for API clients (currently effectively empty)
└── tests/
    ├── web/                    # Main UI tests
    ├── test_data/              # Test data (for example, users.json)
    └── api/                    # Reserved for API tests (currently effectively empty)
```

> Architecture note:
> - `tests/api` is intentionally present to clearly represent the future API test layer. At the moment it is functionally empty (only technical `__init__.py` exists).
> - `src/clients` is intentionally present for future API client wrappers and is currently empty.

### Detailed Test Run Instructions

#### 1) Prepare environment

macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install allure-pytest
python -m playwright install chromium
```

Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install allure-pytest
python -m playwright install --with-deps chromium
```

#### 2) Prepare test data

User credentials file: `tests/test_data/users.json`.

This file is a placeholder: before running tests, replace it with valid `email` and `password` values.

The `random_user` fixture picks a random user from that file. If there is only one user, that same account is used every time.

#### 3) (Optional) set custom environment URL

Default URL is `https://portal.servers.com`.

To override:

```bash
export WEB_BASE_URL="https://your-env.example.com"
```

#### 4) Run all tests

```bash
pytest
```

#### 5) Run specific suites

```bash
pytest tests/web/login
pytest tests/web/platform
pytest tests/web/platform/test_navigation.py -k submenu -v
```

#### 6) Run with proxy (if needed)

The project includes `--proxy` option:

```bash
pytest --proxy
pytest --proxy="socks5://127.0.0.1:9050"
```

### Generate Allure Report

`pytest.ini` is already configured to save results into `allure-results`.

#### 1) Generate test result files

```bash
pytest
```

#### 2) Ensure Allure CLI is installed

macOS (Homebrew):

```bash
brew install allure
```

Linux (npm):

```bash
npm install -g allure-commandline
```

#### 3) Open interactive report

```bash
allure serve allure-results
```

#### 4) Build static report

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

---

## Limitations

In the current implementation, the suite mostly covers **positive scenarios**.

Soon after automated runs against the platform started, the current IP address was blocked, so proxy-based execution was adopted for stable test runs.

The ability to run on **Firefox** and **WebKit** is preserved, but those runs were not validated because there was only one test user available and the tests were written, debugged, and executed through Tor SOCKS, which significantly affected page load times and consequently test execution time.

The project also uses **`playwright.sync_api`** because only one test user was available, and no additional users were created without full knowledge of environment-specific constraints.

Parallel test execution was not implemented due to the constraints mentioned above + quality implementation with preserved test isolation would have significantly increased the time required to complete the test assignment.

Nevertheless, I would be happy to discuss solution options for these issues and how I would implement a more scalable testing framework for the platform if there were no time and resource constraints.


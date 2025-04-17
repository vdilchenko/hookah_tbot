FROM python:3.12.2 as builder

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VENV=/opr/poetry-venv

# Устанавливаем Poetry
RUN pip install poetry==2.1.2

# Копируем зависимости
WORKDIR /api

COPY pyproject.toml poetry.lock ./
COPY README.md ./

ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Устанавливаем зависимости в виртуальное окружение
RUN poetry install --no-root

COPY run_bot.py .
COPY app ./app

CMD ["poetry", "run", "python", "run_bot.py"]
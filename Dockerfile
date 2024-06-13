
FROM python:3.12


RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN pip install poetry

RUN mkdir /app

WORKDIR /app


COPY pyproject.toml poetry.lock ./
COPY src ./src


RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi


COPY .env .env


ENV PYTHONPATH=/app


EXPOSE 8080


CMD ["python", "src/app.py"]

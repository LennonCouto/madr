FROM python:3.14-slim
WORKDIR /app

RUN pip install poetry && \
    poetry config virtualenvs.create false

COPY . .

RUN poetry install --no-interaction --no-ansi --without dev

EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

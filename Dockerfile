FROM python:3.10

WORKDIR /app

COPY . /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN pip install poetry==1.7.1

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

EXPOSE 5000

CMD ["uvicorn", "my_parser.main:app", "--host", "0.0.0.0", "--port", "5000"]
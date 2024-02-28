FROM python:3.10

WORKDIR /app

ADD . /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN pip install poetry==1.7.1

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

EXPOSE 5000

CMD ["python", "my_parser/parser.py"]
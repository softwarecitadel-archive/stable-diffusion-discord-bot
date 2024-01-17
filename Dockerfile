FROM python:3.11

RUN pip install poetry

WORKDIR /project

COPY poetry.lock pyproject.toml /project/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . /project

CMD python bot.py
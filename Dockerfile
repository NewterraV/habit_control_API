FROM python:3.11
LABEL authors="Vladislav_Poroshin"

# Конфигурация пакетного менеджера Poetry
#ENV POETRY_VERSION=1.6.1
#ENV POETRY_HOME=/opt/poetry
#ENV POETRY_VENV=/opt/poetry-venv
#ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
#RUN python3 -m venv $POETRY_VENV \
#    && $POETRY_VENV/bin/pip install -U pip setuptools \
#    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}
#RUN pip install "poetry==$POETRY_VERSION"

# Добавление `poetry` в PATH
#ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

# Установка зависимостей
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

# Применение миграций
CMD ["python3", "manage.py", "migrate"]

#ENTRYPOINT ["top", "-b"]

CMD ["python3", "manage.py", "runserver", "127.0.0.1:8000"]

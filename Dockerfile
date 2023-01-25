FROM python:3.10

WORKDIR /app

# Download and unzip chrome driver
RUN apt-get update
RUN apt-get install curl p7zip-full
RUN mkdir -p /path
RUN curl -sSL https://chromedriver.storage.googleapis.com/110.0.5481.30/chromedriver_linux64.zip -o /path/chromedriver_linux64.zip
RUN 7z x /path/chromedriver_linux64.zip
ENV PATH="${PATH}:/path"

# Install poetry
RUN mkdir -p /poetry
ENV POETRY_HOME="/poetry"
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV POETRY_VIRTUALENVS_CREATE="false"

COPY ./README.md .
COPY ./LICENSE .
COPY ./pyproject.toml .
COPY ./poetry.lock .
COPY ./src .

RUN /poetry/bin/poetry install --only=main
CMD /poetry/bin/poetry run python3 -m crunchyroll_calendar

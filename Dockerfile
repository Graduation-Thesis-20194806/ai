FROM python:3.12.6-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/app

COPY . .

# Install python package
RUN pip3 install poetry
RUN poetry install
RUN poetry run pip install 'litellm[proxy]'
RUN poetry run pip uninstall cryptography -y
RUN poetry run pip install cryptography

CMD ["poetry", "run", "start"]
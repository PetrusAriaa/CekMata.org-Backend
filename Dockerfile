FROM python:3.10.12-slim
WORKDIR /app

COPY Pipfile .

RUN \
    apt update && \
    # apt install gcc g++ -y && \
    pip install --upgrade pip && \
    apt install pipenv -y && \
    pipenv install -d && \
    apt autoremove && apt autoclean
    # pipenv shell && \
    # virtualenv .venv && \
    # .venv/bin/activate && \
    # source $(pipenv --venv)/bin/activate
    # pip install torch -f https://download.pytorch.org/whl/cpu/torch-1.13.1%2Bcpu-cp310-cp310-linux_x86_64.whl &&\
    # pip install torchvision -f https://download.pytorch.org/whl/torchvision-0.1.6-py3-none-any.whl && \
    # pip install -r requirements.txt --no-cache-dir

COPY . .
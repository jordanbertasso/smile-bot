FROM python:3.9.5-buster AS builder

WORKDIR /bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-u", "-m", "bot"]

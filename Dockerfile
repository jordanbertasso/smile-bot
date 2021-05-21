FROM python:3.9.5-buster AS builder

WORKDIR /bot

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "-u", "-m", "bot"]

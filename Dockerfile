FROM python:3.9.16-slim
ENV PYTHONUNBUFFERED 1

RUN mkdir candybot
WORKDIR /candybot
ADD . /candybot
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
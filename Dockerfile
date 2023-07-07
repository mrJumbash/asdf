FROM python:3.10

ENV PYTHONWRYTEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /ss

COPY ./requirements.txt /ss/

RUN pip install -r /ss/requirements.txt

ADD . /ss/
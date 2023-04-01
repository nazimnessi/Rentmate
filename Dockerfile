FROM python:3.8 

RUN apt-get update \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /rentmate 

WORKDIR /rentmate

COPY . /rentmate 

RUN pip install --no-cache-dir --upgrade -r requirements.txt
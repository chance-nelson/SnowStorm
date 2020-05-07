FROM python:3.8-alpine

RUN apk add libcurl curl-dev gcc musl-dev linux-headers

ENV PYCURL_SSL_LIBRARY=openssl

COPY ./requirements.txt /

# upgrade pip and install required python packages
RUN pip install --upgrade cython
RUN pip install -r /requirements.txt
RUN pip install uwsgi

COPY ./ /

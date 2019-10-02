FROM python:3.7-alpine

COPY ./ /

RUN apk add mariadb-dev libcurl curl-dev gcc musl-dev

ENV PYCURL_SSL_LIBRARY=openssl

# upgrade pip and install required python packages
RUN pip install --upgrade cython
RUN pip install -r /requirements.txt
RUN pip install gunicorn

FROM ubuntu:14.04

RUN mkdir /fluentnao
WORKDIR /fluentnao
COPY . /fluentnao

RUN apt-get update && apt-get install -y \
    python-pip \
    libpython2.7 \
    libboost1.55-all-dev \
    python-pygments \
;

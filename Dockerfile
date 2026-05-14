FROM ubuntu:14.04

RUN mkdir /fluentnao
WORKDIR /fluentnao
COPY . /fluentnao

RUN apt-get update && apt-get install -y \
    python-pip \
    libpython2.7 \
    libboost1.55-all-dev \
    python-pygments \
    openssh-client \
    libav-tools \
    imagemagick \
;

ARG USER_ID
ARG GROUP_ID

RUN groupadd -g ${GROUP_ID} nao && \
    useradd -u ${USER_ID} -g nao -m nao

USER nao
WORKDIR /fluentnao

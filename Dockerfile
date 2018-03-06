FROM ubuntu:16.04
MAINTAINER Tom Bech "tom.bech@sesam.io"

ENV DEBIAN_FRONTEND noninteractive

RUN \
apt-get update && \
apt-get install -y \
  locales

RUN localedef -i en_US -f UTF-8 en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
RUN locale-gen en_US.UTF-8
RUN dpkg-reconfigure locales
ENV PYTHONIOENCODING UTF-8

RUN \
apt-get update && \
apt-get install -y \
  build-essential \
  curl \
  python3 \
  python3-dev \
  software-properties-common \
  && \
apt-get clean all && \
apt-get -y autoremove --purge && \
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN curl -sSL https://bootstrap.pypa.io/get-pip.py | python3

ADD ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./service /service
WORKDIR /service
EXPOSE 5000/tcp
ENTRYPOINT ["python3"]
CMD ["service.py"]

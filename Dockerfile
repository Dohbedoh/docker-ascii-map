FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python3 python3-pip
RUN update-ca-certificates -f
RUN pip3 install docker-py

COPY src/docker-ascii-map.py /usr/local/bin/

CMD python3 /usr/local/bin/docker-ascii-map.py

FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python3 python3-pip
RUN update-ca-certificates -f
RUN pip3 install docker-py

COPY . /usr/local/src/docker-ascii-map
RUN cd /usr/local/src/docker-ascii-map && python3 setup.py install

CMD /usr/local/bin/docker-ascii-map.py

FROM debian:wheezy

MAINTAINER Kord Campbell <kordless@stackgeek.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -qq && \
	apt-get install -y -q --no-install-recommends \
	python2.7 python-pip build-essential python-dev

RUN pip install Flask Flask-Cache

RUN apt-get clean && \
	rm -rf /var/lib/apt/lists/*

COPY server.py /server.py
COPY static/* /static/

ENTRYPOINT ["python", "server.py"]

EXPOSE 5000

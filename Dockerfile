FROM python:3.6-alpine
MAINTAINER Haije Ploeg <ploeg.haije@gmail.com>
ENV PS1="\[\e[0;33m\]|> smx10fanctl <| \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "

WORKDIR /src
COPY . /src
RUN pip install --no-cache-dir -r requirements.txt \
    && python setup.py install
WORKDIR /
ENTRYPOINT ["smx10fanctl"]

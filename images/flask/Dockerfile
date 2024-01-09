FROM python:3.10

SHELL ["/bin/bash", "-c", "-l"]

RUN mkdir /tmp/uploads

WORKDIR /root

# bootstrap script to setup and start app
COPY ./bootstrap.sh .
RUN chmod +x ./bootstrap.sh

CMD ./bootstrap.sh
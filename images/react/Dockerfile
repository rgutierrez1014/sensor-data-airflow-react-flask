FROM node:18

SHELL ["/bin/bash", "-c", "-l"]

WORKDIR /root

# bootstrap script to setup and start app
COPY ./bootstrap.sh .
RUN chmod +x ./bootstrap.sh

CMD ./bootstrap.sh